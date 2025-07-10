@echo off
REM install.bat - Windows installation script

echo 🚀 Installing Proxidize: Proxy Tester...
echo ======================================

REM Check if Python is available
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Error: Python 3.7+ is required but not found.
    echo Please install Python 3.7 or higher from https://python.org
    echo Make sure to add Python to your PATH during installation.
    pause
    exit /b 1
)

REM Get Python version
for /f "tokens=2" %%i in ('python --version') do set PYTHON_VERSION=%%i
echo 📋 Detected Python version: %PYTHON_VERSION%

REM Check if pip is available
python -m pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Error: pip is not available.
    echo Please reinstall Python with pip included.
    pause
    exit /b 1
)

echo ✅ Python and pip are available

REM Upgrade pip, setuptools, and wheel
echo 📦 Upgrading pip, setuptools, and wheel...
python -m pip install --upgrade pip setuptools wheel
if %errorlevel% neq 0 (
    echo ⚠️ Warning: Failed to upgrade pip tools, continuing anyway...
)

REM Install the package in development mode
echo 🔧 Installing Proxidize in development mode...
python -m pip install -e .
if %errorlevel% neq 0 (
    echo ❌ Installation failed.
    pause
    exit /b 1
)

REM Verify installation
echo 🧪 Verifying installation...
proxidize --help >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Installation successful!
    echo.
    echo 🎉 Proxidize is now installed and ready to use!
    echo.
    echo Usage examples:
    echo   proxidize --help
    echo   proxidize data\working_http_proxies.txt --http --geo
    echo   proxy-tester data\working_socks_proxies.txt --sock --speed-test
    echo   pxt "proxy.example.com:8080:user:pass" --http
    echo.
    echo For more information, see: README.md
) else (
    echo ❌ Installation verification failed.
    echo The 'proxidize' command is not available.
    echo You may need to restart your command prompt or check your Python Scripts directory in PATH.
    echo.
    echo Try running: python -m src.main --help
)

echo.
echo Press any key to continue...
pause >nul
