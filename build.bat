@echo off

REM Check if Windows
IF NOT "%OS%"=="Windows_NT" (
    echo This script is only for Windows
    exit /b 1
)

REM Check if venv exists
IF NOT EXIST ".\venv" (
    echo venv not found
    echo Setting up venv
    python -m venv venv
    call .\venv\Scripts\activate
    echo Installing dependencies
    pip install -r requirements.txt
    echo venv setup complete!!
)

echo venv found, activating
call .\venv\Scripts\activate
echo Installing dependencies
pip install -r requirements.txt

REM Check if build folder exists
pyinstaller --onefile .\ntscraper.py

REM Remove build folder, cache, and spec file
rmdir /s /q .\build
del .\ntscraper.spec

exit /b 0