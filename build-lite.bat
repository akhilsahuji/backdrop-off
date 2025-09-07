@echo off
REM Optimized build script for Windows - creates smaller executable

echo Building optimized Backdrop-Off executable...
echo This may take several minutes...

REM Create virtual environment if it doesn't exist
if not exist venv-lite (
    echo Creating lightweight virtual environment...
    python -m venv venv-lite
)

REM Activate virtual environment
call venv-lite\Scripts\activate

REM Install minimal dependencies
echo Installing minimal dependencies...
pip install --no-cache-dir -r requirements-lite.txt
pip install pyinstaller

REM Build optimized executable
echo Building executable with size optimizations...
pyinstaller ^
    --onefile ^
    --windowed ^
    --name=Backdrop-Off-Lite ^
    --hidden-import=customtkinter ^
    --hidden-import=PIL._tkinter_finder ^
    --hidden-import=PIL.Image ^
    --hidden-import=rembg ^
    --hidden-import=onnxruntime ^
    --hidden-import=tkinter.colorchooser ^
    --hidden-import=tkinter.filedialog ^
    --hidden-import=tkinter.messagebox ^
    --exclude-module=matplotlib ^
    --exclude-module=scipy ^
    --exclude-module=pandas ^
    --exclude-module=jupyter ^
    --exclude-module=notebook ^
    --exclude-module=IPython ^
    --exclude-module=pytest ^
    --exclude-module=setuptools ^
    --exclude-module=distutils ^
    --exclude-module=unittest ^
    --exclude-module=sqlite3 ^
    --exclude-module=multiprocessing ^
    --exclude-module=asyncio ^
    --exclude-module=logging ^
    --exclude-module=email ^
    --exclude-module=html ^
    --exclude-module=http ^
    --exclude-module=xml ^
    --strip ^
    --noconfirm ^
    --clean ^
    bg_remover_ui.py

echo.
echo Build complete!

REM Show file size
if exist dist\Backdrop-Off-Lite.exe (
    echo Optimized executable created:
    dir dist\Backdrop-Off-Lite.exe
    echo.
    echo To run: dist\Backdrop-Off-Lite.exe
)

echo.
echo Size optimization tips applied:
echo ✓ Excluded unnecessary modules
echo ✓ CPU-only ONNX Runtime
echo ✓ Minimal dependencies
echo ✓ Stripped debug symbols
echo - UPX compression (install UPX for even smaller size)

pause
