@echo off
cd /d "%~dp0"

echo [INFO] Installing required packages...
pip install -r requirements.txt

echo.
echo [INFO] Starting bot...
python bot.py
pause
