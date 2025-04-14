@echo off
echo Starting local server...
cd /d "%~dp0"
python -m http.server 3000
start http://localhost:3000