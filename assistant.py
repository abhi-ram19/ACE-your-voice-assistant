import sounddevice as sd
from scipy.io.wavfile import write
import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import pyjokes
import os
import sys
import tempfile
import numpy as np
import requests
import webbrowser

# Initialize TTS engine
engine = pyttsx3.init()
engine.setProperty('rate', 170)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

# Personal info
your_name = "Abhiram"
your_about = "Abhiram is a passionate AI student skilled in Python, web development, and creating smart assistants like me!"

def talk(text):
    print("🎙️ ACE:", text)
    engine.say(text)
    engine.runAndWait()

def take_command():
    try:
        fs = 44100
        duration = 5
        talk("Listening now... 🎧")
        recording = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='float32')
        sd.wait()

        # Convert to 16-bit PCM
        recording_int16 = np.int16(recording * 32767)

        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmpfile:
            write(tmpfile.name, fs, recording_int16)
            tmp_path = tmpfile.name

        r = sr.Recognizer()
        with sr.AudioFile(tmp_path) as source:
            audio = r.record(source)
            command = r.recognize_google(audio).lower()
            print("🗣️ You said:", command)
            return command

    except sr.UnknownValueError:
        talk("Sorry bro, I couldn’t understand.")
        return ""
    except sr.RequestError:
        talk("Network issue with Google service.")
        return ""
    except Exception as e:
        talk(f"Error: {e}")
        return ""

def get_weather():
    try:
        response = requests.get("https://wttr.in/?format=3")
        if response.status_code == 200:
            talk("Here's the current weather:")
            talk(response.text)
        else:
            talk("Sorry, I couldn’t fetch the weather.")
    except:
        talk("Weather service failed.")

def take_note():
    talk("What should I write down?")
    note = take_command()
    if note:
        with open("note.txt", "a") as f:
            f.write(f"{datetime.datetime.now()}: {note}\n")
        talk("Got it. Noted down!")
    else:
        talk("Nothing was heard to note.")

def run_ace():
    command = take_command()

    if "play" in command:
        song = command.replace("play", "")
        talk("Playing on YouTube 🎶")
        pywhatkit.playonyt(song)

    elif "what's the time" in command:
        time = datetime.datetime.now().strftime('%I:%M %p')
        talk(f"It’s {time} ⏰")

    elif "who is" in command:
        if your_name.lower() in command:
            talk(your_about)
        else:
            person = command.replace("who is", "").strip()
            try:
                info = wikipedia.summary(person, sentences=1)
                talk(info)
            except:
                talk("Sorry, I couldn’t find information about that person.")

    elif "joke" in command:
        talk(pyjokes.get_joke())

    elif "open chrome" in command:
        chrome_path = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
        if os.path.exists(chrome_path):
            talk("Opening Chrome 🚀")
            os.startfile(chrome_path)
        else:
            talk("Chrome not found 😬")

    elif "open code" in command or "open vs code" in command:
        talk("Opening VS Code 💻")
        os.system("code")

    elif "search for" in command:
        query = command.replace("search for", "").strip()
        talk(f"Searching for {query}")
        pywhatkit.search(query)

    elif "open chat gpt" in command:
        webbrowser.open("https://chat.openai.com")
        talk("Opening ChatGPT 💬")

    elif "open gmail" in command:
        webbrowser.open("https://mail.google.com")
        talk("Opening Gmail 📧")

    elif "open instagram" in command:
        webbrowser.open("https://instagram.com")
        talk("Opening Instagram 📸")

    elif "weather" in command:
        get_weather()

    elif "note" in command or "remember this" in command:
        take_note()

    elif "exit" in command or "stop" in command:
        talk("Okay bro, see you later 👋")
        sys.exit()

    elif command != "":
        talk("I heard you, but I don’t understand that yet 😅")

talk("HEY! I'm ACE – your upgraded voice assistant ")

while True:
    run_ace()

#to reactive# ACE will keep running until you say "exit" or "stop"
# Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
# venv\Scripts\activate
# python assistant.py