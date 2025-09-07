@echo off
REM Build script for Windows

echo Building Backdrop-Off for Windows...

REM Create virtual environment if it doesn't exist
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
call venv\Scripts\activate

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt
pip install pyinstaller

REM Build executable
echo Building executable...
pyinstaller backdrop-off.spec

echo Build complete! Check the 'dist' folder for your executable.
echo.
echo To run the executable:
echo   dist\Backdrop-Off.exe

pause
