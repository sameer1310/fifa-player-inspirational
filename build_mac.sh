#!/bin/bash
# ─────────────────────────────────────────────────────────────────────────────
# build_mac.sh  –  Build FIFAInspirational.app for macOS
# ─────────────────────────────────────────────────────────────────────────────
set -e

echo ">> Creating virtual environment (Python 3.12 required for Tkinter)..."
python3.12 -m venv .venv
source .venv/bin/activate

echo ">> Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo ">> Running PyInstaller..."
pyinstaller fifa_mac.spec --clean

echo ""
echo "✅  Build complete: dist/FIFAInspirational.app"
echo "    Drag it to your Applications folder to install."
