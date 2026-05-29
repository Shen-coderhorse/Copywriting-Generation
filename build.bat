@echo off
chcp 65001 >nul
echo ============================================
echo   每日治愈文案生成器 - 打包工具
echo ============================================
echo.

echo [1/3] 检查 PyInstaller...
pip show pyinstaller >nul 2>&1
if %errorlevel% neq 0 (
    echo 正在安装 PyInstaller...
    pip install pyinstaller
)

echo [2/3] 开始打包...
pyinstaller --noconfirm --console --name "每日治愈文案生成器" ^
  --add-data "static;static" ^
  --hidden-import=flask ^
  --hidden-import=flask_cors ^
  --hidden-import=openai ^
  --hidden-import=apscheduler ^
  --hidden-import=docx ^
  --hidden-import=PyPDF2 ^
  app.py

echo.
echo [3/3] 打包完成！
echo.
echo 生成的文件在 dist 文件夹中
echo 双击 dist\每日治愈文案生成器.exe 即可运行
echo.
echo ============================================
echo   手机安装方法：
echo   1. 电脑运行 exe 后，手机浏览器访问显示的地址
echo   2. 点击浏览器菜单「添加到主屏幕」
echo   3. 即可在手机桌面像 APP 一样使用
echo ============================================
echo.
pause
