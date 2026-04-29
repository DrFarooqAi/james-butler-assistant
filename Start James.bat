@echo off
cd /d "%~dp0backend"
start "" "chrome.exe" "http://127.0.0.1:5000"
start "" "ngrok" "http" "--url=your-static-domain.ngrok-free.app" "5000"
python app.py
