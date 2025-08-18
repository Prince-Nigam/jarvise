import pyttsx3
import speech_recognition as sr
import eel
import time
import speech_recognition as sr

def speak(text):
    text = str(text)
    engine = pyttsx3.init('sapi5')
    voices = engine.getProperty('voices') 
    engine.setProperty('voice', voices[0].id)
    engine.setProperty('rate', 174)
    eel.DisplayMessage(text)
    engine.say(text)
    eel.receiverText(text)
    engine.runAndWait()


def takecommand():

    r = sr.Recognizer()

    try:
      with sr.Microphone() as source:
        print('listening....')
        eel.DisplayMessage('listening....')
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source, 1)
        
        audio = r.listen(source, timeout=10, phrase_time_limit=6)

        print('recognizing')
        eel.DisplayMessage('recognizing....')
        query = r.recognize_google(audio, language='en-in')
        print(f"user said: {query}")
        speak(query)
        eel.DisplayMessage(query)
        time.sleep(2)
        return query.lower()
       
    except Exception as e:
        print(f"Recognition Error: {e}")
        return ""
    
    


@eel.expose
def allCommands(message=1):
    if message == 1:
        query = takecommand()
        if query == "":
            eel.senderText("Didn't catch that. Try again.")
            eel.ShowHood()
            return
        eel.senderText(query)
    else:
        query = message
        eel.senderText(query)

    try:
        if "open" in query:
            from engine.features import openCommand
            openCommand(query)
        elif "on youtube" in query:
            from engine.features import PlayYoutube
            PlayYoutube(query)
        elif "send message" in query or "phone call" in query or "video call" in query:
            from engine.features import findContact, whatsApp, makeCall, sendMessage
            contact_no, name = findContact(query)
            if contact_no != 0:
                speak("Which mode you want to use, WhatsApp or mobile?")
                preferance = takecommand()

                if "mobile" in preferance:
                    if "send message" in query or "send sms" in query:
                        speak("What message to send?")
                        message = takecommand()
                        sendMessage(message, contact_no, name)
                    elif "phone call" in query:
                        makeCall(name, contact_no)
                    else:
                        speak("Please try again")
                elif "whatsapp" in preferance:
                    message = ""
                    if "send message" in query:
                        message = 'message'
                        speak("What message to send?")
                        query = takecommand()
                    elif "phone call" in query:
                        message = 'call'
                    else:
                        message = 'video call'

                    whatsApp(contact_no, query, message, name)
        else:
            from engine.features import chatBot
            chatBot(query)

    except Exception as e:
        print(f"Error: {e}")

    eel.ShowHood()