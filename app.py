import os
import sys
import webbrowser
import tempfile
import socket
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from apscheduler.schedulers.background import BackgroundScheduler
import db
import generator

ALLOWED_EXTENSIONS = {'docx', 'pdf', 'txt'}


def _get_static_folder():
    if getattr(sys, 'frozen', False):
        base = getattr(sys, '_MEIPASS', os.path.dirname(sys.executable))
        return os.path.join(base, "static")
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), "static")


app = Flask(__name__, static_folder=_get_static_folder(), static_url_path="")
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
CORS(app)


@app.errorhandler(Exception)
def handle_exception(e):
    import traceback
    tb = traceback.format_exc()
    print(f"[ERROR] {type(e).__name__}: {e}\n{tb}")
    return jsonify({"success": False, "error": f"{type(e).__name__}: {str(e)}"}), 500


@app.errorhandler(404)
def handle_404(e):
    return jsonify({"success": False, "error": "接口不存在"}), 404

scheduler = BackgroundScheduler()
auto_generate_callback = None


@app.route("/")
def index():
    return send_from_directory(app.static_folder, "index.html")


@app.route("/manifest.json")
def manifest():
    return send_from_directory(app.static_folder, "manifest.json", mimetype="application/json")


@app.route("/sw.js")
def service_worker():
    return send_from_directory(app.static_folder, "sw.js", mimetype="application/javascript")


@app.route("/icons/<path:filename>")
def icon_files(filename):
    return send_from_directory(os.path.join(app.static_folder, "icons"), filename)


@app.route("/api/generate", methods=["POST"])
def api_generate():
    try:
        data = request.json or {}
        mode = data.get("mode", "morning")

        result, error = generator.generate_copywriting(mode)
        if error:
            return jsonify({"success": False, "error": error})

        parsed = generator.parse_and_build(result, mode)

        date_key = generator.get_date_key()
        db.save_copywriting(
            date_key, parsed["greeting"], parsed["body"], parsed["tags"], parsed["full_text"], mode
        )

        return jsonify({"success": True, "data": parsed})
    except Exception as e:
        import traceback
        tb = traceback.format_exc()
        print(f"[GENERATE_ERROR] {type(e).__name__}: {e}\n{tb}")
        return jsonify({"success": False, "error": f"生成失败: {str(e)}"}), 500


@app.route("/api/today", methods=["GET"])
def api_today():
    mode = request.args.get("mode", "morning")
    date_key = generator.get_date_key()
    existing = db.get_today_exists(date_key, mode)
    if existing:
        return jsonify({"success": True, "data": existing, "cached": True})
    return jsonify({"success": True, "data": None, "cached": False})


@app.route("/api/history", methods=["GET"])
def api_history():
    days = request.args.get("days", 365, type=int)
    records = db.get_history(days)
    return jsonify({"success": True, "data": records})


@app.route("/api/config", methods=["GET"])
def api_get_config():
    configs = db.get_all_configs()
    if "api_key" in configs and configs["api_key"]:
        configs["api_key"] = configs["api_key"][:8] + "..." + configs["api_key"][-4:]
    return jsonify({"success": True, "data": configs})


@app.route("/api/config", methods=["POST"])
def api_set_config():
    data = request.json
    if not data:
        return jsonify({"success": False, "error": "无数据"})

    current_key = db.get_config("api_key", "")
    for k, v in data.items():
        if k == "api_key" and v.endswith("..."):
            continue
        db.set_config(k, v)

    if "schedule_time" in data:
        _update_schedule(data["schedule_time"])

    return jsonify({"success": True})


@app.route("/api/knowledge", methods=["GET"])
def api_get_knowledge():
    items = db.get_all_knowledge()
    return jsonify({"success": True, "data": items})


@app.route("/api/knowledge", methods=["POST"])
def api_add_knowledge():
    if 'file' not in request.files:
        data = request.json
        if not data or "filename" not in data or "content" not in data:
            return jsonify({"success": False, "error": "请上传文件或提供文本内容"})
        db.save_knowledge(data["filename"], data["content"])
        return jsonify({"success": True})

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"success": False, "error": "未选择文件"})

    ext = file.filename.rsplit(".", 1)[-1].lower() if "." in file.filename else ""
    if ext not in ALLOWED_EXTENSIONS:
        return jsonify({"success": False, "error": f"不支持的文件格式，仅支持 {', '.join(ALLOWED_EXTENSIONS)}"})

    content = extract_file_content(file, ext)
    if content is None:
        return jsonify({"success": False, "error": "文件解析失败"})

    db.save_knowledge(file.filename, content)
    return jsonify({"success": True})


@app.route("/api/knowledge/<int:kid>", methods=["DELETE"])
def api_delete_knowledge(kid):
    db.delete_knowledge(kid)
    return jsonify({"success": True})


@app.route("/api/knowledge/<int:kid>", methods=["GET"])
def api_get_knowledge_detail(kid):
    content = db.get_knowledge_content(kid)
    if content is None:
        return jsonify({"success": False, "error": "未找到"})
    return jsonify({"success": True, "data": {"content": content}})


@app.route("/api/tags", methods=["GET"])
def api_get_tags():
    tags = db.get_config("tags", ",".join(generator.DEFAULT_TAGS))
    return jsonify({"success": True, "data": tags})


@app.route("/api/schedule", methods=["POST"])
def api_set_schedule():
    data = request.json
    time_str = data.get("time", "08:00")
    db.set_config("schedule_time", time_str)
    _update_schedule(time_str)
    return jsonify({"success": True})


def _update_schedule(time_str):
    global auto_generate_callback
    try:
        hour, minute = time_str.split(":")
        scheduler.remove_all_jobs()
        if auto_generate_callback:
            scheduler.add_job(auto_generate_callback, "cron", hour=int(hour), minute=int(minute))
    except Exception:
        pass


def start_scheduler(callback=None):
    global auto_generate_callback
    auto_generate_callback = callback
    time_str = db.get_config("schedule_time", "08:00")
    _update_schedule(time_str)
    scheduler.start()


def extract_file_content(file_storage, ext):
    try:
        if ext == "txt":
            raw = file_storage.read()
            for enc in ["utf-8", "gbk", "gb2312", "latin-1"]:
                try:
                    return raw.decode(enc)
                except (UnicodeDecodeError, LookupError):
                    continue
            return raw.decode("utf-8", errors="ignore")

        if ext == "docx":
            from docx import Document
            with tempfile.NamedTemporaryFile(suffix=".docx", delete=False) as tmp:
                tmp.write(file_storage.read())
                tmp_path = tmp.name
            try:
                doc = Document(tmp_path)
                paragraphs = [p.text for p in doc.paragraphs if p.text.strip()]
                return "\n".join(paragraphs)
            finally:
                os.unlink(tmp_path)

        if ext == "pdf":
            from PyPDF2 import PdfReader
            with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
                tmp.write(file_storage.read())
                tmp_path = tmp.name
            try:
                reader = PdfReader(tmp_path)
                texts = []
                for page in reader.pages:
                    t = page.extract_text()
                    if t and t.strip():
                        texts.append(t.strip())
                return "\n".join(texts)
            finally:
                os.unlink(tmp_path)

    except Exception as e:
        print(f"文件解析错误: {e}")
        return None

    return None


def _get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"


def run_server(host="0.0.0.0", port=5280):
    db.init_db()
    start_scheduler()

    local_ip = _get_local_ip()
    print("=" * 50)
    print("  ✨ 每日治愈文案生成器已启动")
    print("=" * 50)
    print(f"  �️  电脑访问: http://localhost:{port}")
    print(f"  📱 手机访问: http://{local_ip}:{port}")
    print(f"  📱 手机浏览器打开后，点击「添加到主屏幕」即可安装APP")
    print("=" * 50)
    print("  关闭此窗口即可停止服务")
    print("=" * 50)

    webbrowser.open(f"http://localhost:{port}")
    app.run(host=host, port=port, debug=False, threaded=True)


if __name__ == "__main__":
    run_server()
