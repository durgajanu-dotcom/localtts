# Local TTS App

Small local Text-to-Speech app using Flask and pyttsx3.

Quick start (PowerShell):

```powershell
python -m venv .venv
. .\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python app.py
```

Run as a one-click desktop app (Windows)

1. Install `pyinstaller` into the venv: `pip install pyinstaller`
2. Run the build script from project root in PowerShell:

```powershell
.\build_exe.ps1
```

This will produce a single-file executable in `dist\start_app.exe`. Copy that file to your desktop and double-click to run the app  it will start the web server and open the UI in your default browser.

Notes
- The bundled exe includes `templates` and `output` folders via PyInstaller `--add-data` flags in `build_exe.ps1`.
- The app supports client-side speed control (0.75x to 2.0x) and server-side speed control when using "Play on Server".

