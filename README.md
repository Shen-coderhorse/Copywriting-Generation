<p align="center">
  <img src="https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=A%20magical%20sparkling%20star%20with%20gentle%20golden%20light%20rays%20on%20dark%20blue%20gradient%20background,%20minimalist%20flat%20design,%20app%20icon%20style&image_size=square" width="120" alt="Logo">
</p>

<h1 align="center">✨ 每日治愈文案生成器</h1>

<p align="center">
  <strong>一键生成抖音风格治愈文案 · 三端通用 · AI 驱动</strong>
</p>

<p align="center">
  <a href="#功能特性">特性</a> •
  <a href="#快速开始">快速开始</a> •
  <a href="#运行方式">运行方式</a> •
  <a href="#技术架构">架构</a> •
  <a href="#项目结构">结构</a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.11+-blue.svg" alt="Python">
  <img src="https://img.shields.io/badge/Flask-RESTful-green.svg" alt="Flask">
  <img src="https://img.shields.io/badge/OpenAI-Compatible-API-orange.svg" alt="OpenAI API">
  <img src="https://img.shields.io/badge/Capacitor-Android-purple.svg" alt="Capacitor">
  <img src="https://img.shields.io/badge/License-MIT-red.svg" alt="License">
</p>

---

## 功能特性

| 特性 | 说明 |
|------|------|
| 🤖 **AI 智能生成** | 支持 OpenAI 兼容 API（DeepSeek / 通义千问 / ChatGPT 等） |
| 📝 **知识库上传** | 上传 `.docx` / `.pdf` / `.txt` 文件，AI 学习你的风格 |
| 🌅 **早安 & 晚安** | 一键切换模式，自动匹配日期与星期 |
| 🔄 **历史记录** | 自动保存所有生成结果，支持复制与回溯 |
| 💾 **本地存储** | 所有数据本地 SQLite 数据库，无需联网（除 AI 调用外） |
| 🖥️ **桌面双栏布局** | 左侧文案展示 + 右侧功能面板，充分利用屏幕空间 |
| 📱 **手机原生体验** | Capacitor 封装 Android APK，支持 PWA 安装到主屏 |

---

## 快速开始

### 环境要求

```
Python ≥ 3.11    Node.js ≥ 18    Java ≥ 21 (仅打包 APK 时需要)
```

### 安装依赖

```bash
pip install -r requirements.txt
cd mobile-app && npm install
```

---

## 运行方式

本项目支持 **3 种运行方式**，满足不同场景需求：

### 方式一：双击 EXE（推荐 · 最简单）

> 无需安装任何环境，下载即用。

```
dist/CopywritingApp.exe    ← 双击即可运行
```

窗口自动打开，内置 Flask 服务 + pywebview 桌面窗口。

### 方式二：浏览器访问 Localhost

```bash
python app.py
# 浏览器打开 http://localhost:5280
```

适合开发调试，支持热更新前端代码。

### 方式三：手机 APK 安装

```
dist/每日治愈文案.apk    ← 传到手机安装
```

独立运行，直接调用 AI API，不依赖后端服务。也支持 **PWA 安装到主屏**（通过浏览器访问后添加到主屏幕）。

---

## 技术架构

```
┌─────────────────────────────────────────────────────┐
│                    前端展示层                         │
│  ┌──────────────────┐   ┌───────────────────┐      │
│  │  static/index.html│   │ mobile-app/www/   │      │
│  │  (桌面端 · 双栏)   │   │ (手机端 · 单栏)    │      │
│  └────────┬─────────┘   └────────┬──────────┘      │
│           │ fetch / API          │ 直接调用          │
├───────────┼──────────────────────┼─────────────────┤
│           ▼                      ▼                  │
│  ┌────────────────┐   ┌──────────────────┐         │
│  │  Flask 后端     │   │  OpenAI 兼容 API  │         │
│  │  app.py        │   │  DeepSeek/通义等  │         │
│  ├────────────────┤   └──────────────────┘         │
│  │ generator.py   │                                │
│  │ db.py (SQLite)  │                                │
│  └────────────────┘                                │
│                                                     │
│  ┌────────────────┐   ┌──────────────────┐         │
│  │ desktop.py     │   │ Capacitor + Gradle│         │
│  │ → pywebview    │   │ → Android APK     │         │
│  │ → PyInstaller  │   │                   │         │
│  └───────┬────────┘   └────────┬─────────┘         │
│          │                      │                    │
│          ▼                      ▼                    │
│    CopywritingApp.exe     每日治愈文案.apk           │
└─────────────────────────────────────────────────────┘
```

### 核心模块

| 模块 | 文件 | 职责 |
|------|------|------|
| **Web 后端** | `app.py` | Flask RESTful API、文件解析、PWA 路由 |
| **AI 引擎** | `generator.py` | Prompt 构建、OpenAI SDK 调用、客户端缓存复用、本地模板降级 |
| **数据层** | `db.py` | SQLite 配置/知识库/历史 CRUD，PyInstaller 路径兼容 |
| **桌面入口** | `desktop.py` | pywebview 窗口管理、自动端口分配、数据库初始化 |
| **桌面前端** | `static/index.html` | 双栏响应式布局、拖拽上传、Toast 提示 |
| **手机前端** | `mobile-app/www/index.html` | 移动端单栏 UI、localStorage 存储、JSZip/pdf.js 解析文件 |

---

## 项目结构

```
Copywriting Generation/
├── app.py                  # Flask 主服务 (API 路由 + 文件解析)
├── db.py                   # SQLite 数据库层
├── generator.py            # AI 文案生成引擎
├── desktop.py              # pywebview 桌面窗口入口
├── requirements.txt        # Python 依赖
├── build.bat               # PyInstaller 一键打包脚本
├── .gitignore
│
├── static/                 # 桌面端前端资源
│   ├── index.html          # 主页面 (双栏布局)
│   ├── manifest.json       # PWA 配置
│   ├── sw.js               # Service Worker (离线缓存)
│   └── icons/               # PWA 图标 (72px ~ 512px)
│
├── data/                   # 运行时数据目录
│   └── copywriting.db      # SQLite 数据库 (自动创建)
│
├── dist/                   # 构建产物
│   ├── CopywritingApp.exe  # Windows 桌面版 (~27MB)
│   └── 每日治愈文案.apk    # Android 手机版 (~3.6MB)
│
└── mobile-app/             # 手机端项目
    ├── www/
    │   └── index.html      # 手机端页面 (独立前端)
    ├── android/            # Capacitor Android 项目
    ├── capacitor.config.json
    ├── package.json
    └── package-lock.json
```

---

## AI 接口配置

本项目使用 **OpenAI 兼容协议**，支持所有兼容接口：

| 提供商 | Base URL 示例 | 支持模型 |
|--------|-------------|---------|
| OpenAI | `https://api.openai.com/v1` | gpt-4o, gpt-4o-mini |
| DeepSeek | `https://api.deepseek.com` | deepseek-chat |
| 阿里通义千问 | `https://dashscope.aliyuncs.com/compatible-mode/v1` | qwen-plus, qwen-max, qwen3.5-flash |
| 硅基流动 | `https://api.siliconflow.cn/v1` | 多种开源模型 |

> ⚡ 已优化：默认关闭思考模型 (`enable_thinking: false`)，生成速度提升 **6 倍+**

---

## 开发指南

### 打包 Windows EXE

```bash
# 使用 venv311 虚拟环境中的 PyInstaller
.\venv311\Scripts\pyinstaller.exe --noconfirm --onefile --windowed ^
  --name "CopywritingApp" --add-data "static;static" ^
  --hidden-import=flask --hidden-import=flask_cors ^
  --hidden-import=openai --hidden-import=apscheduler ^
  --hidden-import=docx --hidden-import=PyPDF2 ^
  --hidden-import=pywebview desktop.py
# 输出: dist/CopywritingApp.exe
```

### 打包 Android APK

```bash
cd mobile-app
npx cap sync android
# 设置环境变量:
#   JAVA_HOME=E:\configuration\Java\jdk21
#   ANDROID_HOME=C:\Users\<用户名>\AppData\Local\Android\Sdk
D:\gradle-8.2.1\bin\gradle.bat assembleDebug --no-daemon
# 输出: android/app/build/outputs/apk/debug/app-debug.apk
```

### 本地开发调试

```bash
# 启动 Flask (多线程模式，端口 5280)
python app.py

# 或指定端口
python -c "from app import app; app.run(host='127.0.0.1', port=5280, debug=False, threaded=True)"
```

---

## 性能优化记录

| 问题 | 根因 | 优化方案 | 效果 |
|------|------|---------|------|
| 生成卡死 | `generate()` 无 try-catch | 添加 try-catch-finally + 60s AbortController 超时 | 不再永久 loading |
| 生成返回 HTML | Flask 异常返回默认 HTML 页 | 全局 `@errorhandler(Exception)` 返回 JSON | 错误信息正确显示 |
| EXE 无法使用 | `desktop.py` 未调用 `db.init_db()` | 启动前初始化数据库 | EXE 正常工作 |
| API 调用慢 49s | qwen3.5 默认开启思考模式 | `enable_thinking: False` | **6倍提速** |
| 文案千篇一律 | Prompt 强制固定 5 行格式 | 改为自由风格 + 多样化示例 + temperature=1.0 | 每次风格不同 |
| Flask 单线程阻塞 | `app.run()` 默认单线程 | 添加 `threaded=True` | 并发请求不再排队 |
| 客户端重复创建 | 每次 API 调用新建 OpenAI Client | `_client_cache` 缓存复用 | 省去 ~200ms/次 |

---

## 技术栈

```
后端:  Python 3.11 · Flask · Flask-CORS · OpenAI Python SDK · APScheduler · python-docx · PyPDF2
前端:  Vanilla HTML/CSS/JS (无框架) · CSS Variables · Flexbox 响应式
桌面:  PyInstaller (--onefile) · pywebview (WebView2)
手机:  Capacitor 6 · Android SDK 34 · Gradle 8.2.1 · JSZip · pdf.js
数据:  SQLite (APScheduler 定时任务) / localStorage (手机端)
图标:  AI Generated via Trae API
```

---

<p align="center">
  Made with ✨ by <b>Shen</b> · 2026
</p>
