import os
import sys
import threading
import time
import socket
import webview

from app import app


def find_free_port():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("127.0.0.1", 0))
    port = s.getsockname()[1]
    s.close()
    return port


if __name__ == "__main__":
    port = find_free_port()

    import db
    db.init_db()

    flask_thread = threading.Thread(
        target=lambda: app.run(host="127.0.0.1", port=port, debug=False, use_reloader=False, threaded=True),
        daemon=True,
    )
    flask_thread.start()
    time.sleep(1.5)

    window = webview.create_window(
        "每日治愈文案生成器",
        f"http://127.0.0.1:{port}",
        width=1200,
        height=800,
        resizable=True,
        min_size=(900, 600),
    )
    webview.start()
