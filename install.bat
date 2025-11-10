@echo off
echo Installing Production QR Code Generator Dependencies...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python from https://python.org
    pause
    exit /b 1
)

echo Python found. Installing required packages...
echo.

REM Install required packages
pip install qrcode[pil]==7.4.2
if errorlevel 1 (
    echo Error installing qrcode
    pause
    exit /b 1
)

pip install Pillow==10.1.0
if errorlevel 1 (
    echo Error installing Pillow
    pause
    exit /b 1
)

echo.
echo ✅ Installation complete!
echo.
echo You can now run:
echo   • GUI: python qr_generator_gui.py
echo   • CLI: python qr_generator_cli.py --help
echo   • Examples: python examples.py
echo.
pause