import speech_recognition as sr
from gtts import gTTS
import pygame
import wikipedia
import webbrowser
import datetime
import os

# Initialize the recognizer
recognizer = sr.Recognizer()

# Initialize pygame mixer
pygame.mixer.init()

def speak(text):
    """Convert text to speech using gTTS and play it using pygame."""
    tts = gTTS(text=text, lang='en')
    filename = "voice.mp3"
    tts.save(filename)
    pygame.mixer.music.load(filename)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)  # Adjust tick rate to control playback
    pygame.mixer.music.stop()  # Stop the playback
    pygame.mixer.music.unload()  # Unload the music
    os.remove(filename)  # Delete the file after it's no longer in use

def listen():
    """Capture audio from the microphone and recognize it."""
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
        try:
            print("Recognizing...")
            query = recognizer.recognize_google(audio, language='en-US')
            print(f"User said: {query}")
        except sr.UnknownValueError:
            speak("Sorry, I did not understand that.")
            return "None"
        except sr.RequestError:
            speak("Sorry, my speech service is down.")
            return "None"
    return query.lower()

def get_wikipedia_summary(query):
    """Fetch summary from Wikipedia."""
    results = wikipedia.summary(query, sentences=2)
    return results

def open_website(url):
    """Open a website in the default web browser."""
    webbrowser.open(url)

def tell_time():
    """Tell the current time."""
    now = datetime.datetime.now()
    return now.strftime("%H:%M:%S")

def main():
    speak("Hello! How can I assist you today?")
    while True:
        query = listen()

        if 'wikipedia' in query:
            speak("Searching Wikipedia...")
            query = query.replace("wikipedia", "")
            try:
                result = get_wikipedia_summary(query)
                speak("According to Wikipedia")
                speak(result)
            except wikipedia.exceptions.DisambiguationError:
                speak("There are multiple results. Please be more specific.")
            except wikipedia.exceptions.PageError:
                speak("I couldn't find any results on Wikipedia.")

        elif 'open youtube' in query:
            speak("Opening YouTube")
            open_website("https://www.youtube.com")

        elif 'open google' in query:
            speak("Opening Google")
            open_website("https://www.google.com")

        elif 'time' in query:
            current_time = tell_time()
            speak(f"The current time is {current_time}")

        elif 'exit' in query or 'bye' in query or 'quit' in query:
            speak("Goodbye!")
            break

        else:
            speak("I am sorry, I didn't catch that. Can you please repeat?")

if __name__ == "__main__":
    main()
