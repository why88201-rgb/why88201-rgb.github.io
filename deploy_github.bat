@echo off
chcp 65001 >nul
echo ========================================
echo 快速部署到GitHub脚本
echo ========================================
echo.

echo [1/4] 检查Git环境...
git --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未检测到Git，请先安装Git
    pause
    exit /b 1
)
echo [OK] Git环境正常

echo.
echo [2/4] 运行部署前检查...
python check_deployment.py
if errorlevel 1 (
    echo.
    echo [错误] 部署检查未通过，请修复后再部署
    pause
    exit /b 1
)

echo.
echo [3/4] 初始化Git仓库...
if exist ".git" (
    echo [OK] Git仓库已存在
) else (
    git init
    echo [OK] Git仓库初始化完成
)

echo.
echo [4/4] 添加和提交文件...
git add .
git status
echo.
set /p commit_msg="请输入提交信息 (默认: 'Update: 项目更新'): "
if "%commit_msg%"=="" set commit_msg=Update: 项目更新
git commit -m "%commit_msg%"
echo [OK] 文件已提交

echo.
echo ========================================
echo 下一步操作：
echo ========================================
echo.
echo 1. 在GitHub上创建新仓库
echo 2. 运行以下命令连接到GitHub：
echo    git remote add origin https://github.com/你的用户名/你的仓库名.git
echo    git push -u origin main
echo.
echo 3. 在Render上创建Web Service并连接到GitHub仓库
echo.
echo 详细说明请查看 DEPLOYMENT_REPORT.md 文件
echo ========================================

pause
