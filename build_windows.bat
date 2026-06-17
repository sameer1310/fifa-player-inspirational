@echo off
REM ─────────────────────────────────────────────────────────────────────────
REM build_windows.bat  -  Build FIFAInspirational.exe for Windows
REM Run this from the project root in a regular Command Prompt or PowerShell
REM ─────────────────────────────────────────────────────────────────────────

echo >> Creating virtual environment...
python -m venv .venv
call .venv\Scripts\activate.bat

echo >> Installing dependencies...
pip install --upgrade pip
pip install -r requirements.txt

echo >> Running PyInstaller...
pyinstaller fifa_windows.spec --clean

echo.
echo [OK] Build complete: dist\FIFAInspirational.exe
echo      Copy it anywhere and double-click to run.
pause
