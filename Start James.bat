@echo off
cd /d "%~dp0backend"
echo Starting James...
start "James - Butler Server" python app.py
timeout /t 3 /nobreak >nul
start "" "http://127.0.0.1:5000"
