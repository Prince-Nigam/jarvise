import os
import subprocess
import sys

try:
    import eel
except ModuleNotFoundError:
    eel = None

from engine.auth import Recognize
from engine.command import speak
from engine.init_db import init_database


def _ensure_eel_available():
    if eel is None:
        print("Eel is not installed.")
        print("Run setup.bat first, then run.bat")
        return False
    return True


def _run_device_setup():
    if os.name != "nt" or not os.path.exists("device.bat"):
        return
    try:
        subprocess.call(["cmd", "/c", "device.bat"], shell=False)
    except Exception as exc:
        print(f"Device setup skipped: {exc}")


def _open_browser():
    url = "http://localhost:8000/index.html"
    if os.name == "nt":
        os.system(f'start msedge.exe --app="{url}"')
    else:
        import webbrowser
        webbrowser.open(url)


def start():
    init_database()

    if not _ensure_eel_available():
        sys.exit(1)

    eel.init("www")

    from engine.features import playAssistantSound

    try:
        playAssistantSound()
    except Exception as exc:
        print(f"Startup sound skipped: {exc}")

    @eel.expose
    def init():
        _run_device_setup()
        eel.hideLoader()
        speak("Ready for Face Authentication")
        flag = Recognize.AuthenticateFace()
        if flag == 1:
            eel.hideFaceAuth()
            speak("Face Authentication Successful")
            eel.hideFaceAuthSuccess()
            speak("Hello Sir, Welcome, How can I help you")
            eel.hideStart()
            try:
                playAssistantSound()
            except Exception:
                pass
        else:
            speak("Face Authentication Failed")

    _open_browser()
    eel.start("index.html", mode=None, host="localhost", block=True)


if __name__ == "__main__":
    try:
        start()
    except RuntimeError as exc:
        print(exc)
        sys.exit(1)
