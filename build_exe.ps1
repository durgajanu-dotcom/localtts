# Build a single-file executable for Windows using PyInstaller
# Run this in an elevated PowerShell or regular PowerShell with Python and PyInstaller installed.
# Example:
# 1) Activate your venv (optional): .\.venv\Scripts\Activate.ps1
# 2) pip install pyinstaller
# 3) # Build single-file executable from simple_reader.py with PyInstaller

# Clean any previous builds
Remove-Item -Path .\dist\*, .\build\* -Recurse -Force -ErrorAction SilentlyContinue

# Build the desktop app
.\.venv\Scripts\pyinstaller.exe --onefile --noconsole --name "LocalTTS" simple_reader.py
