import speech_recognition as sr
import pyttsx3
import pyautogui
import webbrowser
import os
import time
import random
import datetime
import pywhatkit
import requests
import pyperclip
import smtplib
from email.mime.text import MIMEText
from bs4 import BeautifulSoup

engine = pyttsx3.init()

def speak(text):
    print(f"[Assistant]: {text}")
    engine.say(text)
    engine.runAndWait()

def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.adjust_for_ambient_noise(source, duration=1)
        audio = r.listen(source)
    try:
        command = r.recognize_google(audio, language='en-in')
        print(f"You said: {command}")
        return command.lower().strip()
    except sr.UnknownValueError:
        speak("Sorry, I didn't understand that.")
    except sr.RequestError:
        speak("Internet connection error.")
    return ""

def type_input():
    command = input("Enter your command: ")
    print(f"You typed: {command}")
    return command.lower().strip()

def play_music():
    music_folder = "C:\\Users\\Public\\Music"  # change if needed
    try:
        songs = os.listdir(music_folder)
        if songs:
            song = random.choice(songs)
            os.startfile(os.path.join(music_folder, song))
            speak(f"Playing music: {song}")
        else:
            speak("No music files found.")
    except:
        speak("Could not play music.")

def tell_time():
    now = datetime.datetime.now()
    speak(f"The time is {now.strftime('%I:%M %p')}")

def tell_date():
    today = datetime.datetime.now()
    speak(f"Today's date is {today.strftime('%A, %d %B %Y')}")

def send_whatsapp_message():
    speak("Say the phone number with country code")
    number = listen().replace(" ", "").replace("+", "")
    number = f"+{number}"
    speak("What is the message?")
    message = listen()
    if message:
        hour = datetime.datetime.now().hour
        minute = datetime.datetime.now().minute + 1
        try:
            pywhatkit.sendwhatmsg(number, message, hour, minute)
            speak("Message scheduled.")
        except Exception as e:
            print(e)
            speak("Failed to send message.")

def send_email():
    speak("Type the recipient's email:")
    to_email = input("Recipient: ")
    speak("What should the email say?")
    body = listen()
    try:
        from_email = "youremail@gmail.com"
        password = "your-app-password"
        msg = MIMEText(body)
        msg['Subject'] = "Voice Assistant Mail"
        msg['From'] = from_email
        msg['To'] = to_email
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(from_email, password)
        server.send_message(msg)
        server.quit()
        speak("Email sent successfully!")
    except Exception as e:
        print(e)
        speak("Failed to send email.")

def get_weather():
    speak("Which city?")
    city = listen()
    api_key = "your_openweather_api_key"
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    try:
        res = requests.get(url).json()
        temp = res['main']['temp']
        desc = res['weather'][0]['description']
        speak(f"Weather in {city}: {temp} degrees and {desc}")
    except:
        speak("Could not retrieve weather.")

def get_news():
    speak("Getting top headlines...")
    try:
        url = 'https://news.google.com/news/rss'
        res = requests.get(url)
        soup = BeautifulSoup(res.content, features='xml')
        headlines = soup.findAll('title')[2:7]
        for h in headlines:
            speak(h.text)
    except:
        speak("Failed to get news.")

def take_screenshot():
    filename = f"screenshot_{int(time.time())}.png"
    pyautogui.screenshot(filename)
    speak(f"Screenshot saved as {filename}")

def read_clipboard():
    text = pyperclip.paste()
    speak(f"Clipboard contains: {text}")

def google_search(command):
    query = command.replace("search for", "").strip()
    url = f"https://www.google.com/search?q={query}"
    webbrowser.open(url)
    speak(f"Searching for {query}")

def play_on_youtube(command):
    song = command.replace("play", "").strip()
    pywhatkit.playonyt(song)
    speak(f"Playing {song} on YouTube")

def execute_command(command):
    if "notepad" in command:
        os.system("notepad")
        speak("Opening Notepad")
    elif "browser" in command or "chrome" in command:
        webbrowser.open("https://www.google.com")
        speak("Opening browser")
    elif "close window" in command:
        pyautogui.hotkey('alt', 'f4')
        speak("Closing window")
    elif "shutdown" in command:
        os.system("shutdown /s /t 1")
        speak("Shutting down")
    elif "restart" in command:
        os.system("shutdown /r /t 1")
        speak("Restarting")
    elif "type" in command:
        text = command.replace("type", "").strip()
        pyautogui.write(text)
        speak(f"Typing: {text}")
    elif "scroll down" in command:
        pyautogui.scroll(-500)
        speak("Scrolling down")
    elif "scroll up" in command:
        pyautogui.scroll(500)
        speak("Scrolling up")
    elif "lock" in command:
        pyautogui.hotkey('win', 'l')
        speak("Locking the computer")
    elif "play music" in command:
        play_music()
    elif "time" in command:
        tell_time()
    elif "date" in command:
        tell_date()
    elif "whatsapp" in command:
        send_whatsapp_message()
    elif "email" in command:
        send_email()
    elif "weather" in command:
        get_weather()
    elif "news" in command:
        get_news()
    elif "screenshot" in command:
        take_screenshot()
    elif "clipboard" in command:
        read_clipboard()
    elif "search for" in command:
        google_search(command)
    elif "play" in command and "youtube" in command:
        play_on_youtube(command)
    elif "exit" in command or "quit" in command or "stop" in command:
        speak("Goodbye!")
        exit()
    else:
        speak("Command not recognized.")

if __name__ == "__main__":
    speak("Voice assistant activated.")
    while True:
        speak("Would you like to give a command by voice or by typing?")
        method = input("Choose input method (voice / type): ").lower().strip()
        if "voice" in method:
            cmd = listen()
        elif "type" in method:
            cmd = type_input()
        else:
            speak("Invalid input mode. Say or type voice or type.")
            continue

        if cmd:
            execute_command(cmd)