<div align="center">

<br>

<a href="https://github.com/Shen-coderhorse/Copywriting-Generation">
  <img src="https://img.shields.io/badge/%E6%AF%8F%E6%97%A5%E6%B2%BB%E7%96%97%E6%96%87%E6%A1%88%E7%94%9F%E6%88%90%E5%99%A8-FF4D6D?style=for-the-badge&logo=data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyNCAyNCIgZmlsbD0id2hpdGUiPjxwYXRoIGQ9Ik0xMiAwTDIuNSA1LjdMMTIgMTZMjEuNSA1LjdMMTIgMFoiLz48L3N2Zz4=&logoColor=white" alt="Logo">
</a>

<h3>
  <i>一键生成抖音风格治愈文案 · AI 驱动 · 三端通用</i>
</h3>

<br>

<img src="https://img.shields.io/badge/Python-3.11+-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python">
<img src="https://img.shields.io/badge/Flask-RESTful-000000?style=flat-square&logo=flask&logoColor=white" alt="Flask">
<img src="https://img.shields.io/badge/OpenAI-Compatible-FF6B35?style=flat-square&logo=openai&logoColor=white" alt="OpenAI">
<img src="https://img.shields.io/badge/PyInstaller-EXE-green?style=flat-square&logo=python&logoColor=white" alt="EXE">
<img src="https://img.shields.io/badge/Capacitor-APK-481F99?style=flat-square&logo=capacitor&logoColor=white" alt="Capacitor">
<img src="https://img.shields.io/badge/License-MIT-D1D5DB?style=flat-square" alt="License">

<br><br>

<a href="#-功能特性"><strong>📋 功能特性</strong></a>
&nbsp;·&nbsp;
<a href="#-运行方式"><strong>🚀 运行方式</strong></a>
&nbsp;·&nbsp;
<a href="#-技术架构"><strong>🏗️ 技术架构</strong></a>
&nbsp;·&nbsp;
<a href="#-项目结构"><strong>📂 项目结构</strong></a>
&nbsp;·&nbsp;
<a href="#-开发指南"><strong>⚙️ 开发指南</strong></a>

<br><br>
<br>

</div>

---

## ✦ 功能特性

<table align="center">
<tr>
<td width="50%" valign="top">

### 🤖 AI 智能生成

支持 **OpenAI 兼容协议**，接入即用：

```
DeepSeek  ·  通义千问  ·  ChatGPT  ·  硅基流动
```

自动关闭思考模式，生成速度 **提升 6 倍+**

</td>
<td width="50%" valign="top">

### 📝 知识库学习

上传 `.docx` / `.pdf` / `.txt` 文件

AI 自动学习你的文案风格

生成结果千人千面

</td>
</tr>
<tr>
<td width="50%" valign="top">

### 🌅 双模式切换

**早安** — 温暖启程，元气满满

**晚安** — 卸下疲惫，安然入眠

自动匹配日期与星期

</td>
<td width="50%" valign="top">

### 💾 三端通用

| 平台 | 方式 | 大小 |
|:---:|------|:---:|
| 🖥️ **桌面** | 双击 EXE | ~27 MB |
| 🌐 **浏览器** | `localhost` | - |
| 📱 **手机** | 安装 APK | ~3.6 MB |

</td>
</tr>
<tr>
<td width="50%" valign="top">

### 🎨 桌面双栏布局

```
┌─────────────────────┬──────────┐
│                     │ ⚙️ AI 配置 │
│   ✨ 文案展示区     │ 📁 知识库  │
│                     │ 📜 历史记录 │
│   [复制] [生成]     │          │
└─────────────────────┴──────────┘
```

充分利用屏幕空间，操作一目了然

</td>
<td width="50%" valign="top">

### 🔒 完全本地化

- SQLite 数据库存储所有数据
- 无需联网（除 AI 调用外）
- 历史记录永久保存
- 配置信息持久保留

</td>
</tr>
</table>

---

## ✦ 运行方式

### 🖥️ 方式一：双击 EXE（推荐）

> 零配置，下载即用

```
dist/CopywritingApp.exe    ← 双击运行，窗口自动弹出
```

内置 Flask 服务 + pywebview 桌面窗口，开箱即用。

---

### 🌐 方式二：浏览器访问

```bash
pip install -r requirements.txt
python app.py
# → 浏览器打开 http://localhost:5280
```

适合开发调试，前端代码修改后刷新即可生效。

---

### 📱 方式三：手机 APK 安装

```
dist/每日治愈文案.apk    ← 传到手机安装
```

独立运行，直接调用 AI API。也支持 **PWA 安装到主屏**：

```
浏览器访问 → 添加到主屏幕 → 即刻拥有 App 体验
```

---

## ✦ 技术架构

```
╔══════════════════════════════════════════════════════════════╗
║                      用户交互层                             ║
║                                                           ║
║  ┌──────────────────────┐    ┌────────────────────────┐   ║
║  │                      │    │                        │   ║
║  │   🖥️ 桌面端 (双栏)    │    │   📱 手机端 (单栏)      │   ║
║  │   static/index.html  │    │   mobile-app/www/      │   ║
║  │                      │    │                        │   ║
║  └──────────┬───────────┘    └───────────┬────────────┘   ║
║             │ fetch / REST              │ 直接调用           ║
╠═════════════╪═══════════════════════════╪═══════════════════╣
║             ▼                           ▼                  ║
║  ┌────────────────────────┐   ┌──────────────────────┐   ║
║  │        Flask 后端       │   │  OpenAI 兼容 API      │   ║
║  │  ┌─────────────────┐  │   │                      │   ║
║  │  │ app.py          │  │   │  DeepSeek / 通义千问   │   ║
║  │  ├─────────────────┤  │   │  ChatGPT / 硅基流动    │   ║
║  │  │ generator.py    │◄─┼──►│                      │   ║
║  │  ├─────────────────┤  │   └──────────────────────┘   ║
║  │  │ db.py (SQLite)  │  │                              ║
║  │  └─────────────────┘  │                              ║
║  └──────────┬────────────┘                              ║
║             │                                           ║
║  ┌──────────▼────────────┐   ┌──────────────────────┐   ║
║  │    desktop.py         │   │  Capacitor + Gradle   │   ║
║  │  → pywebview 窗口     │   │  → Android APK       │   ║
║  │  → PyInstaller 打包   │   │                      │   ║
║  └──────────┬────────────┘   └──────────┬───────────┘   ║
║             ▼                           ▼               ║
║     CopywritingApp.exe            每日治愈文案.apk        ║
╚══════════════════════════════════════════════════════════════╝
```

---

## ✦ 核心模块

| 模块 | 文件 | 职责 |
|:---:|------|------|
| 🔧 **Web 后端** | `app.py` | Flask RESTful API · 文件解析 · PWA · 全局错误处理 |
| 🧠 **AI 引擎** | `generator.py` | Prompt 构建 · OpenAI SDK · 客户端缓存 · 本地降级 |
| 💾 **数据层** | `db.py` | SQLite CRUD · PyInstaller 路径兼容 · 自动建表 |
| 🪟 **桌面入口** | `desktop.py` | pywebview 窗口 · 自动端口分配 · 数据库初始化 |
| 🖥️ **桌面前端** | `static/index.html` | 双栏响应式布局 · 拖拽上传 · Toast 提示 |
| 📱 **手机前端** | `mobile-app/www/index.html` | 移动端 UI · localStorage · JSZip/pdf.js |

---

## ✦ 项目结构

```
Copywriting Generation/
│
├── 📄 app.py                 # Flask 主服务
├── 📄 db.py                  # SQLite 数据库层
├── 📄 generator.py           # AI 文案生成引擎
├── 📄 desktop.py             # pywebview 桌面入口
├── 📄 requirements.txt       # Python 依赖
├── 📄 build.bat              # EXE 打包脚本
│
├── 📁 static/                # 桌面前端资源
│   ├── index.html            # 主页面 (双栏布局)
│   ├── manifest.json         # PWA 配置
│   ├── sw.js                 # Service Worker
│   └── icons/                # PWA 图标 (72~512px)
│
├── 📁 data/                  # 运行时数据
│   └── copywriting.db        # SQLite 数据库 (自动创建)
│
├── 📁 dist/                  # 构建交付物
│   ├── CopywritingApp.exe    # 🖥️ Windows 桌面版 (~27MB)
│   └── 每日治愈文案.apk       # 📱 Android 手机版 (~3.6MB)
│
└── 📁 mobile-app/            # 手机端项目
    ├── www/
    │   └── index.html        # 手机端独立前端
    ├── android/              # Capacitor Android 项目
    ├── capacitor.config.json
    └── package.json
```

---

## ✦ AI 接口兼容

本项目使用 **OpenAI 兼容协议**，以下平台均可直接使用：

| 提供商 | Base URL | 推荐模型 |
|:-----:|----------|---------|
| **OpenAI** | `api.openai.com/v1` | gpt-4o · gpt-4o-mini |
| **DeepSeek** | `api.deepseek.com` | deepseek-chat |
| **阿里通义** | `dashscope.aliyuncs.com/.../v1` | qwen-plus · qwen3.5-flash |
| **硅基流动** | `api.siliconflow.cn/v1` | 多种开源模型 |

> 💡 **性能提示**：已默认关闭思考模式 (`enable_thinking: false`)，生成速度提升 **6 倍以上**

---

## ✦ 开发指南

<details open>
<summary><b>📦 打包 Windows EXE</b></summary>

```bash
# 创建虚拟环境 & 安装依赖
python -m venv venv311
.\venv311\Scripts\activate
pip install -r requirements.txt

# PyInstaller 打包
.\venv311\Scripts\pyinstaller.exe --noconfirm --onefile --windowed ^
  --name "CopywritingApp" ^
  --add-data "static;static" ^
  --hidden-import=flask --hidden-import=flask_cors ^
  --hidden-import=openai --hidden-import=apscheduler ^
  --hidden-import=docx --hidden-import=PyPDF2 ^
  --hidden-import=pywebview ^
  desktop.py

# 输出 → dist/CopywritingApp.exe
```
</details>

<details>
<summary><b>📦 打包 Android APK</b></summary>

```bash
cd mobile-app
npm install
npx cap sync android

# 设置环境变量后构建
# JAVA_HOME=E:\configuration\Java\jdk21
# ANDROID_HOME=C:\Users\<用户>\AppData\Local\Android\Sdk
gradle assembleDebug --no-daemon

# 输出 → android/app/build/outputs/apk/debug/app-debug.apk
```
</details>

<details>
<summary><b>🔧 本地开发调试</b></summary>

```bash
# 启动服务 (多线程模式)
python app.py
# → http://localhost:5280

# 或指定端口
python -c "
from app import app, db
db.init_db()
app.run(host='127.0.0.1', port=5280, debug=False, threaded=True)
"
```
</details>

---

## ✦ 性能优化历程

| # | 问题 | 根因 | 修复方案 | 效果 |
|:-:|------|------|---------|:----:|
| 1 | 生成卡死 | `generate()` 无 try-catch | try-catch-finally + AbortController 60s | ✅ 不再卡死 |
| 2 | 返回 HTML | 异常返回 Flask 默认错误页 | 全局 `@errorhandler(Exception)` → JSON | ✅ 错误正确显示 |
| 3 | EXE 无法使用 | `desktop.py` 未初始化数据库 | 启动前调用 `db.init_db()` | ✅ EXE 正常工作 |
| 4 | API 慢 49s | qwen3.5 思考模式开启 | `enable_thinking: False` | ✅ **6倍提速** |
| 5 | 文案雷同 | Prompt 强制固定格式 | 自由风格 + 多样示例 + temperature=1.0 | ✅ 每次不同 |
| 6 | 单线程阻塞 | Flask 默认单线程 | `threaded=True` | ✅ 并发不排队 |
| 7 | 客户端重复创建 | 每次新建 OpenAI Client | `_client_cache` 缓存复用 | ✅ 省 ~200ms/次 |

---

## ✦ 技术栈全景

```
┌─────────────────────────────────────────────────────────┐
│  后端                                                  │
│  Python 3.11  ·  Flask  ·  Flask-CORS  ·  APScheduler   │
│  OpenAI SDK  ·  python-docx  ·  PyPDF2                 │
├─────────────────────────────────────────────────────────┤
│  前端 (桌面)                                           │
│  Vanilla HTML/CSS/JS  ·  CSS Variables  ·  Flexbox      │
│  PWA + Service Worker                                  │
├─────────────────────────────────────────────────────────┤
│  桌面打包                                              │
│  PyInstaller (--onefile)  ·  pywebview (WebView2)       │
├─────────────────────────────────────────────────────────┤
│  手机端                                                │
│  Capacitor 6  ·  Android SDK 34  ·  Gradle 8.2.1       │
│  JSZip  ·  pdf.js  ·  localStorage                    │
├─────────────────────────────────────────────────────────┤
│  数据持久                                              │
│  SQLite (桌面)  ·  localStorage (手机)                   │
└─────────────────────────────────────────────────────────┘
```

---

<p align="center">
  <sub>Made with <span style="color:#FF4D6D">♥</span> by <b>Shen</b> · 2026</sub>
</p>
