@echo off

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    REM Python is not installed, download and install it
    curl -o python_installer.exe https://www.python.org/ftp/python/3.9.5/python-3.9.5-amd64.exe
    python_installer.exe /quiet InstallAllUsers=1 PrependPath=1 Include_test=0
)

REM Install necessary dependencies
pip install requests

REM Run Python script in the background and hide the terminal window
start /B /MIN pythonw.exe "bot.py"