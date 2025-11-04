# Build a single-file executable for Windows using PyInstaller
# Run this in an elevated PowerShell or regular PowerShell with Python and PyInstaller installed.
# Example:
# 1) Activate your venv (optional): .\.venv\Scripts\Activate.ps1
# 2) pip install pyinstaller
# 3) .\build_exe.ps1

pyinstaller --onefile --add-data "templates;templates" --add-data "output;output" start_app.py
