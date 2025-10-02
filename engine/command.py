import speech_recognition as sr
import eel
import time
from gtts import gTTS
import os
import pygame
from googletrans import Translator

# Initialize translator and pygame for audio playback
translator = Translator()
pygame.mixer.init()

# Global language settings
CURRENT_LANGUAGE = "en"  # Default language
CURRENT_LANG_CODE = "en-in"  # For speech recognition

# Language configurations (gTTS supported languages)
LANGUAGES = {
    "english": {"tts": "en", "stt": "en-in", "name": "English"},
    "hindi": {"tts": "hi", "stt": "hi-in", "name": "Hindi"},
    "spanish": {"tts": "es", "stt": "es-es", "name": "Spanish"},
    "french": {"tts": "fr", "stt": "fr-fr", "name": "French"},
    "german": {"tts": "de", "stt": "de-de", "name": "German"},
    "italian": {"tts": "it", "stt": "it-it", "name": "Italian"},
    "portuguese": {"tts": "pt", "stt": "pt-br", "name": "Portuguese"},
    "russian": {"tts": "ru", "stt": "ru-ru", "name": "Russian"},
    "japanese": {"tts": "ja", "stt": "ja-jp", "name": "Japanese"},
    "chinese": {"tts": "zh-cn", "stt": "zh-cn", "name": "Chinese"},
    "arabic": {"tts": "ar", "stt": "ar-sa", "name": "Arabic"},
    "korean": {"tts": "ko", "stt": "ko-kr", "name": "Korean"},
    "tamil": {"tts": "ta", "stt": "ta-in", "name": "Tamil"},
    "telugu": {"tts": "te", "stt": "te-in", "name": "Telugu"},
    "bengali": {"tts": "bn", "stt": "bn-in", "name": "Bengali"},
    "marathi": {"tts": "mr", "stt": "mr-in", "name": "Marathi"},
    "gujarati": {"tts": "gu", "stt": "gu-in", "name": "Gujarati"},
    "kannada": {"tts": "kn", "stt": "kn-in", "name": "Kannada"},
    "malayalam": {"tts": "ml", "stt": "ml-in", "name": "Malayalam"},
    "punjabi": {"tts": "pa", "stt": "pa-in", "name": "Punjabi"},
    "urdu": {"tts": "ur", "stt": "ur-pk", "name": "Urdu"},
    "thai": {"tts": "th", "stt": "th-th", "name": "Thai"},
    "vietnamese": {"tts": "vi", "stt": "vi-vn", "name": "Vietnamese"},
    "indonesian": {"tts": "id", "stt": "id-id", "name": "Indonesian"},
    "dutch": {"tts": "nl", "stt": "nl-nl", "name": "Dutch"},
    "polish": {"tts": "pl", "stt": "pl-pl", "name": "Polish"},
    "turkish": {"tts": "tr", "stt": "tr-tr", "name": "Turkish"},
}


def speak(text, language=None, slow=False):
    """Speak text using Google Text-to-Speech (better multi-language support)"""
    global CURRENT_LANGUAGE
    
    if language and language in LANGUAGES:
        lang_code = LANGUAGES[language]["tts"]
    else:
        lang_code = CURRENT_LANGUAGE
    
    text = str(text)
    
    try:
        # Display message
        eel.DisplayMessage(text)
        eel.receiverText(text)
        
        # Generate speech
        tts = gTTS(text=text, lang=lang_code, slow=slow)
        
        # Save to temporary file
        filename = "temp_audio.mp3"
        tts.save(filename)
        
        # Play audio
        pygame.mixer.music.load(filename)
        pygame.mixer.music.play()
        
        # Wait for audio to finish
        while pygame.mixer.music.get_busy():
            time.sleep(0.1)
        
        # Clean up
        pygame.mixer.music.unload()
        time.sleep(0.2)
        
        if os.path.exists(filename):
            os.remove(filename)
            
    except Exception as e:
        print(f"Speech error: {e}")


def translate_text(text, target_lang):
    """Translate text to target language"""
    try:
        translated = translator.translate(text, dest=target_lang)
        return translated.text
    except Exception as e:
        print(f"Translation error: {e}")
        return text


def takecommand(language=None):
    """Take voice command in specified language"""
    global CURRENT_LANG_CODE
    
    lang_code = language if language else CURRENT_LANG_CODE
    
    r = sr.Recognizer()

    with sr.Microphone() as source:
        print(f'Listening in {lang_code}....')
        eel.DisplayMessage('Listening....')
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source)
        
        audio = r.listen(source, 10, 6)

    try:
        print('Recognizing')
        eel.DisplayMessage('Recognizing....')
        query = r.recognize_google(audio, language=lang_code)
        print(f"User said: {query}")
        eel.DisplayMessage(query)
        time.sleep(2)
        
    except Exception as e:
        print(f"Recognition error: {e}")
        return ""
    
    return query.lower()


def change_language(language_name):
    """Change the assistant's language"""
    global CURRENT_LANGUAGE, CURRENT_LANG_CODE
    
    if language_name in LANGUAGES:
        CURRENT_LANGUAGE = LANGUAGES[language_name]["tts"]
        CURRENT_LANG_CODE = LANGUAGES[language_name]["stt"]
        
        # Speak confirmation in the new language
        confirmation = f"Language changed to {LANGUAGES[language_name]['name']}"
        translated = translate_text(confirmation, CURRENT_LANGUAGE)
        speak(translated)
        return True
    else:
        speak("Sorry, that language is not supported")
        return False


def list_available_languages():
    """List all available languages"""
    lang_list = ", ".join([LANGUAGES[lang]["name"] for lang in LANGUAGES.keys()])
    speak(f"Available languages are: {lang_list}")


@eel.expose
def allCommands(message=1):
    global CURRENT_LANGUAGE, CURRENT_LANG_CODE
    
    if message == 1:
        query = takecommand()
        print(query)
        eel.senderText(query)
    else:
        query = message
        eel.senderText(query)
    
    try:
        # Language change command
        if "change language" in query or "switch language" in query:
            speak("Which language would you like?")
            lang_query = takecommand()
            
            for lang_name in LANGUAGES.keys():
                if lang_name in lang_query:
                    change_language(lang_name)
                    return
            
            speak("Language not recognized. Please try again")
        
        # List languages
        elif "list languages" in query or "available languages" in query:
            list_available_languages()
        
        # Translate command
        elif "translate" in query:
            speak("What would you like me to translate?")
            text_to_translate = takecommand()
            
            speak("To which language?")
            target_lang_query = takecommand()
            
            for lang_name in LANGUAGES.keys():
                if lang_name in target_lang_query:
                    target_lang = LANGUAGES[lang_name]["tts"]
                    translated = translate_text(text_to_translate, target_lang)
                    speak(f"Translation: {translated}", language=lang_name)
                    return
        
        # Open commands
        elif "open" in query or "launch" in query or "start" in query:
            from engine.features import openCommand
            openCommand(query)
        
        # YouTube
        elif "on youtube" in query:
            from engine.features import PlayYoutube
            PlayYoutube(query)
        # Weather command
        elif "weather" in query:
           speak("Please tell me the city name")
           city_name = takecommand()
           if city_name:
             get_weather(city_name)
           else:
              speak("City name not recognized")
        
        # Shutdown PC command
        elif "shutdown" in query or "turn off" in query:
            shutdown_pc()
        # Lock PC command
        elif "lock" in query or "lock pc" in query:
            lock_pc()
        # Take screenshot command
        elif "screenshot" in query or "take screenshot" in query or "capture screen" in query:
            take_screenshot()
        # Volume control
        elif "increase volume" in query:
            increase_volume()
        elif "decrease volume" in query:
            decrease_volume()
        elif "mute volume" in query or "mute" in query:
            mute_volume()
        # Check internet speed
        elif "internet speed" in query or "check internet" in query or "speed test" in query:
            check_internet_speed()
      # Tell the current time
        elif "time" in query or "current time" in query or "tell me the time" in query:
            tell_time()
      # Tell the current date
        elif "date" in query or "current date" in query or "today's date" in query:
           tell_date()
      # Create note
        elif "create note" in query or "take note" in query or "write note" in query:
           speak("What would you like me to write in the note?")
           note_text = takecommand()
           if note_text:
              create_note(note_text)
           else:
             speak("Note text not recognized")
       # Create folder
        elif "create folder" in query or "make folder" in query:
            speak("What should be the folder name?")
            folder_name = takecommand()
            if folder_name:
              create_folder(folder_name)
            else:
               speak("Folder name not recognized")
        # Delete file
        elif "delete file" in query or "remove file" in query:
            speak("Please tell me the full path of the file to delete")
            file_path = takecommand()
    
        # Optional: Clean up voice input (remove "slash", "backslash" words)
            file_path = file_path.replace(" slash ", "/").replace(" backslash ", "\\")
    
            if file_path:
              delete_file(file_path)
            else:
              speak("File path not recognized")
        # Check battery status
        elif "battery" in query or "battery status" in query or "check battery" in query:
           check_battery_status()
        # Sleep PC
        elif "sleep" in query or "sleep pc" in query or "put computer to sleep" in query:
          sleepthepc()

       
        # Communication
        elif "send message" in query or "phone call" in query or "video call" in query:
            from engine.features import findContact, whatsApp, makeCall, sendMessage
            contact_no, name = findContact(query)
            
            if contact_no != 0:
                speak("Which mode you want to use whatsapp or mobile")
                preferance = takecommand()

                if "mobile" in preferance:
                    if "send message" in query or "send sms" in query: 
                        speak("What message to send")
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
                        speak("What message to send")
                        query = takecommand()
                    elif "phone call" in query:
                        message = 'call'
                    else:
                        message = 'video call'
                    
                    whatsApp(contact_no, query, message, name)
        
        # Default: AI response
        else:
            if query.strip():
                from engine.features import geminiai
                geminiai(query)
        
    except Exception as e:
        print(f"Error: {e}")
        speak("Sorry, I encountered an error")
    
    eel.ShowHood()
  

def hotword_listener():
    """Listen for wake word"""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Waiting for wake word...")
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source, phrase_time_limit=3)
    try:
        query = r.recognize_google(audio, language='en-in')
        if "ira" in query.lower():
            speak("Yes, I'm listening")
            allCommands()
    except:
        pass

# Initialize
def initialize():
    """Initialize the assistant"""
    print("Initializing Multi-Language Voice Assistant with gTTS...")
    speak("Voice assistant initialized and ready")
    print(f"Current language: {CURRENT_LANGUAGE}")
    print("Say 'change language' to switch languages")
    print("Say 'list languages' to hear available languages")


if __name__ == "__main__":
    initialize()



import requests

# Add this function to your code
def get_weather(city):
    """Fetch weather information for a city"""
    API_KEY = "90946428f9d789855734d6b3501f9978"  # Replace with your API key
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
        response = requests.get(url)
        data = response.json()

        if data["cod"] != 200:
            speak(f"Sorry, I could not find weather information for {city}")
            return

        weather_desc = data["weather"][0]["description"]
        temp = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        wind_speed = data["wind"]["speed"]

        weather_report = (f"Weather in {city}: {weather_desc}. "
                          f"Temperature: {temp}°C. "
                          f"Humidity: {humidity}%. "
                          f"Wind speed: {wind_speed} m/s.")
        speak(weather_report)

    except Exception as e:
        print(f"Weather error: {e}")
        speak("Sorry, I couldn't fetch the weather right now.")

import os
import platform

def shutdown_pc():
    """Shutdown the PC safely"""
    try:
        speak("Shutting down the computer in 10 seconds. Please save your work.")
        system_os = platform.system()

        if system_os == "Windows":
            os.system("shutdown /s /t 10")  # Shutdown after 10 seconds
        elif system_os == "Linux" or system_os == "Darwin":  # macOS = Darwin
            os.system("shutdown now")
        else:
            speak("Sorry, I cannot shutdown this operating system")
    except Exception as e:
        print(f"Shutdown error: {e}")
        speak("Sorry, I could not shutdown the PC")



import ctypes

def lock_pc():
    """Lock the PC"""
    try:
        system_os = platform.system()
        
        if system_os == "Windows":
            ctypes.windll.user32.LockWorkStation()
            speak("PC is now locked.")
        elif system_os == "Linux":
            os.system("gnome-screensaver-command -l")  # For GNOME-based Linux
            speak("PC is now locked.")
        elif system_os == "Darwin":  # macOS
            os.system("/System/Library/CoreServices/Menu\\ Extras/User.menu/Contents/Resources/CGSession -suspend")
            speak("Mac is now locked.")
        else:
            speak("Sorry, I cannot lock this operating system.")
    except Exception as e:
        print(f"Lock PC error: {e}")
        speak("Sorry, I could not lock the PC.")


import pyautogui
import datetime

def take_screenshot():
    """Take a screenshot and save it"""
    try:
        # Create a timestamped filename
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"screenshot_{timestamp}.png"
        
        # Take screenshot
        screenshot = pyautogui.screenshot()
        screenshot.save(filename)
        
        speak(f"Screenshot taken and saved as {filename}")
    except Exception as e:
        print(f"Screenshot error: {e}")
        speak("Sorry, I could not take the screenshot.")



from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

# Initialize volume control
def get_volume_interface():
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(
        IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    return volume

def increase_volume():
    """Increase system volume by 10%"""
    try:
        volume = get_volume_interface()
        current = volume.GetMasterVolumeLevelScalar()
        new = min(current + 0.1, 1.0)
        volume.SetMasterVolumeLevelScalar(new, None)
        speak(f"Volume increased to {int(new*100)} percent")
    except Exception as e:
        print(f"Increase volume error: {e}")
        speak("Sorry, I could not increase the volume.")

def decrease_volume():
    """Decrease system volume by 10%"""
    try:
        volume = get_volume_interface()
        current = volume.GetMasterVolumeLevelScalar()
        new = max(current - 0.1, 0.0)
        volume.SetMasterVolumeLevelScalar(new, None)
        speak(f"Volume decreased to {int(new*100)} percent")
    except Exception as e:
        print(f"Decrease volume error: {e}")
        speak("Sorry, I could not decrease the volume.")

def mute_volume():
    """Mute system volume"""
    try:
        volume = get_volume_interface()
        volume.SetMute(1, None)
        speak("Volume muted")
    except Exception as e:
        print(f"Mute volume error: {e}")
        speak("Sorry, I could not mute the volume.")


import speedtest

def check_internet_speed():
    """Check internet speed and speak results"""
    try:
        speak("Checking internet speed. This may take a few seconds.")
        st = speedtest.Speedtest()
        st.get_best_server()
        download_speed = st.download() / 1_000_000  # Convert to Mbps
        upload_speed = st.upload() / 1_000_000      # Convert to Mbps
        ping = st.results.ping

        speak(f"Your internet speed is as follows. Download speed: {download_speed:.2f} Mbps. "
              f"Upload speed: {upload_speed:.2f} Mbps. Ping: {ping} milliseconds.")
    except Exception as e:
        print(f"Internet speed error: {e}")
        speak("Sorry, I could not check the internet speed right now.")


import datetime

def tell_time():
    """Speak the current time"""
    try:
        now = datetime.datetime.now()
        current_time = now.strftime("%I:%M %p")  # Example: 03:45 PM
        speak(f"The current time is {current_time}")
    except Exception as e:
        print(f"Tell time error: {e}")
        speak("Sorry, I could not tell the time right now.")


def tell_date():
    """Speak the current date"""
    try:
        now = datetime.datetime.now()
        current_date = now.strftime("%A, %d %B %Y")  # Example: Wednesday, 02 October 2025
        speak(f"Today's date is {current_date}")
    except Exception as e:
        print(f"Tell date error: {e}")
        speak("Sorry, I could not tell the date right now.")
  



def create_note(text):
    """Create a note with the given text and save it in Notes folder"""
    try:
        # Folder to save notes
        notes_folder = os.path.join(os.path.expanduser("~"), "Documents", "AssistantNotes")
        os.makedirs(notes_folder, exist_ok=True)

        # Create a timestamped filename
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = os.path.join(notes_folder, f"note_{timestamp}.txt")

        # Write the note
        with open(filename, "w", encoding="utf-8") as f:
            f.write(text)

        speak(f"Note saved successfully in {filename}")
    except Exception as e:
        print(f"Create note error: {e}")
        speak("Sorry, I could not create the note.")




def create_folder(folder_name):
    """Create a folder in the user's Documents directory"""
    try:
        # Base path (Documents folder)
        base_path = os.path.join(os.path.expanduser("~"), "Documents")
        folder_path = os.path.join(base_path, folder_name)

        # Create folder
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
            speak(f"Folder '{folder_name}' created successfully in Documents.")
        else:
            speak(f"Folder '{folder_name}' already exists in Documents.")
    except Exception as e:
        print(f"Create folder error: {e}")
        speak("Sorry, I could not create the folder.")




def delete_file(file_path):
    """Delete a file at the given path"""
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            speak(f"File {os.path.basename(file_path)} has been deleted successfully.")
        else:
            speak("Sorry, the file does not exist.")
    except Exception as e:
        print(f"Delete file error: {e}")
        speak("Sorry, I could not delete the file.")


import psutil

def check_battery_status():
    """Check and speak battery percentage and charging status"""
    try:
        battery = psutil.sensors_battery()
        if battery:
            percent = battery.percent
            plugged = battery.power_plugged
            status = "charging" if plugged else "not charging"
            speak(f"The battery is at {percent} percent and is currently {status}.")
        else:
            speak("Sorry, I could not detect battery information.")
    except Exception as e:
        print(f"Battery status error: {e}")
        speak("Sorry, I could not check the battery status.")




def sleepthepc():
    """Put the PC to sleep"""
    try:
        speak("Putting the computer to sleep.")
        # Windows sleep command
        os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
    except Exception as e:
        print(f"Sleep PC error: {e}")
        speak("Sorry, I could not put the PC to sleep.")
