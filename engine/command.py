import time

try:
    import pyttsx3
except ModuleNotFoundError:
    pyttsx3 = None

try:
    import speech_recognition as sr
except ModuleNotFoundError:
    sr = None

try:
    import eel
except ModuleNotFoundError:
    eel = None


def _eel_call(name, *args):
    if eel is None:
        return
    fn = getattr(eel, name, None)
    if fn is not None:
        fn(*args)


def speak(text):
    text = str(text)
    if pyttsx3 is None:
        print(text)
        return

    engine = pyttsx3.init("sapi5")
    voices = engine.getProperty("voices")
    if voices:
        engine.setProperty("voice", voices[0].id)
    engine.setProperty("rate", 174)
    _eel_call("DisplayMessage", text)
    engine.say(text)
    _eel_call("receiverText", text)
    engine.runAndWait()


def takecommand():
    if sr is None:
        return ""

    r = sr.Recognizer()

    try:
        with sr.Microphone() as source:
            print("listening....")
            _eel_call("DisplayMessage", "listening....")
            r.pause_threshold = 1
            r.adjust_for_ambient_noise(source, 1)
            audio = r.listen(source, timeout=10, phrase_time_limit=6)
    except Exception as exc:
        print(f"Microphone error: {exc}")
        return ""

    try:
        print("recognizing")
        _eel_call("DisplayMessage", "recognizing....")
        query = r.recognize_google(audio, language="en-in")
        print(f"user said: {query}")
        speak(query)
        _eel_call("DisplayMessage", query)
        time.sleep(2)
        return query.lower()
    except Exception as exc:
        print(f"Recognition Error: {exc}")
        return ""


if eel is not None:
    expose = eel.expose
else:
    def expose(func):
        return func


@expose
def allCommands(message=1):
    if message == 1:
        query = takecommand()
        if query == "":
            _eel_call("senderText", "Didn't catch that. Try again.")
            _eel_call("ShowHood")
            return
        _eel_call("senderText", query)
    else:
        query = message
        _eel_call("senderText", query)

    try:
        if "open" in query:
            from engine.features import openCommand

            openCommand(query)
        elif "on youtube" in query:
            from engine.features import PlayYoutube

            PlayYoutube(query)
        elif (
            "send message" in query
            or "phone call" in query
            or "video call" in query
        ):
            from engine.features import findContact, makeCall, sendMessage, whatsApp

            contact_no, name = findContact(query)
            if contact_no != 0:
                speak("Which mode you want to use, WhatsApp or mobile?")
                preferance = takecommand()

                if "mobile" in preferance:
                    if "send message" in query or "send sms" in query:
                        speak("What message to send?")
                        msg = takecommand()
                        sendMessage(msg, contact_no, name)
                    elif "phone call" in query:
                        makeCall(name, contact_no)
                    else:
                        speak("Please try again")
                elif "whatsapp" in preferance:
                    msg = ""
                    if "send message" in query:
                        msg = "message"
                        speak("What message to send?")
                        query = takecommand()
                    elif "phone call" in query:
                        msg = "call"
                    else:
                        msg = "video call"

                    whatsApp(contact_no, query, msg, name)
        else:
            from engine.features import chatBot

            chatBot(query)
    except Exception as exc:
        print(f"Error: {exc}")

    _eel_call("ShowHood")
