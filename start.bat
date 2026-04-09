@echo off
chcp 65001 >nul
echo ========================================
echo 白水Jimmy Official 网站启动脚本
echo ========================================
echo.

echo [1/3] 检查Python环境...
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未检测到Python，请先安装Python 3.11+
    pause
    exit /b 1
)
echo [OK] Python环境正常

echo.
echo [2/3] 检查依赖...
pip show Flask >nul 2>&1
if errorlevel 1 (
    echo [!] 依赖未安装，正在安装...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo [错误] 依赖安装失败
        pause
        exit /b 1
    )
) else (
    echo [OK] 依赖已安装
)

echo.
echo [3/3] 检查数据文件...
if not exist "data\uploaded_files.json" (
    echo [!] 数据文件不存在，正在初始化...
    python init_data.py
) else (
    echo [OK] 数据文件已存在
)

echo.
echo ========================================
echo 启动网站...
echo ========================================
echo.
echo 访问地址：
echo   - 本地: http://127.0.0.1:5000
echo   - 局域网: http://192.168.3.106:5000
echo.
echo 管理员账户：
echo   - 用户名: admin
echo   - 密码: admin123
echo.
echo 按 Ctrl+C 停止服务器
echo ========================================
echo.

python app.py

pause
