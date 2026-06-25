import os
import socket
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


def safe_call_js_function(name, *args):
    if eel is None:
        return False

    try:
        callback = getattr(eel, name)
    except AttributeError:
        return False

    if not callable(callback):
        return False

    try:
        callback(*args)
        return True
    except Exception as exc:
        print(f"Skipping JS function {name}: {exc}")
        return False


def _run_device_setup():
    if os.name != "nt" or not os.path.exists("device.bat"):
        return
    try:
        subprocess.call(["cmd", "/c", "device.bat"], shell=False)
    except Exception as exc:
        print(f"Device setup skipped: {exc}")


def _find_free_port(start_port=8000):
    port = start_port
    while True:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            try:
                sock.bind(("localhost", port))
                return port
            except OSError:
                port += 1


def _open_browser(port):
    url = f"http://localhost:{port}/index.html"
    try:
        if os.name == "nt":
            os.startfile(url)
            return
    except Exception as exc:
        print(f"Default browser launch skipped: {exc}")

    try:
        import webbrowser
        webbrowser.open(url)
    except Exception as exc:
        print(f"Browser launch skipped: {exc}")


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
        safe_call_js_function("hideLoader")
        speak("Ready for Face Authentication")
        flag = Recognize.AuthenticateFace()
        if flag == 1:
            safe_call_js_function("hideFaceAuth")
            speak("Face Authentication Successful")
            safe_call_js_function("hideFaceAuthSuccess")
            speak("Hello Sir, Welcome, How can I help you")
            safe_call_js_function("hideStart")
            try:
                playAssistantSound()
            except Exception:
                pass
        else:
            speak("Face Authentication Failed")

    port = _find_free_port()
    print(f"Starting Jarvis UI at http://127.0.0.1:{port}/index.html")
    _open_browser(port)

    try:
        eel.start("index.html", mode=None, host="127.0.0.1", block=True, port=port)
    except Exception as exc:
        print(f"Eel startup failed: {exc}")
        sys.exit(1)


if __name__ == "__main__":
    try:
        start()
    except RuntimeError as exc:
        print(exc)
        sys.exit(1)
