import speech_recognition as sr
import eel
import time
from gtts import gTTS
import os
import pygame
from googletrans import Translator
import requests
import platform
import ctypes
import pyautogui
import datetime
import speedtest
import psutil
import winshell
import wikipedia
import threading
import string
import shutil
from pathlib import Path


# Initialize translator and pygame for audio playback
translator = Translator()
pygame.mixer.init()

# Global language settings
CURRENT_LANGUAGE = "en"
CURRENT_LANG_CODE = "en-in"

# Language configurations
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

# Configuration
TODO_FILE = "todo.txt"
WEATHER_API_KEY = "90946428f9d789855734d6b3501f9978"
reminders = []


def speak(text, language=None, slow=False):
    """Speak text using Google Text-to-Speech"""
    global CURRENT_LANGUAGE
    
    if language and language in LANGUAGES:
        lang_code = LANGUAGES[language]["tts"]
    else:
        lang_code = CURRENT_LANGUAGE
    
    text = str(text)
    
    try:
        eel.DisplayMessage(text)
        eel.receiverText(text)
        
        tts = gTTS(text=text, lang=lang_code, slow=slow)
        filename = "temp_audio.mp3"
        tts.save(filename)
        
        pygame.mixer.music.load(filename)
        pygame.mixer.music.play()
        
        while pygame.mixer.music.get_busy():
            time.sleep(0.1)
        
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
        
        try:
            audio = r.listen(source, timeout=10, phrase_time_limit=6)
        except sr.WaitTimeoutError:
            print("Listening timed out")
            return ""

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
        
        confirmation = f"Language changed to {LANGUAGES[language_name]['name']}"
        translated = translate_text(confirmation, CURRENT_LANGUAGE)
        speak(translated)
        return True
    else:
        speak("Sorry, that language is not supported")
        return False


def list_available_languages():
    """List all available languages"""
    lang_list = ", ".join([LANGUAGES[lang]["name"] for lang in list(LANGUAGES.keys())[:10]])
    speak(f"Available languages include: {lang_list}, and more")


def get_weather(city):
    """Fetch weather information for a city"""
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric"
        response = requests.get(url, timeout=10)
        data = response.json()

        if data.get("cod") != 200:
            speak(f"Sorry, I could not find weather information for {city}")
            return

        weather_desc = data["weather"][0]["description"]
        temp = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        wind_speed = data["wind"]["speed"]

        weather_report = (f"Weather in {city}: {weather_desc}. "
                          f"Temperature: {temp} degrees Celsius. "
                          f"Humidity: {humidity} percent. "
                          f"Wind speed: {wind_speed} meters per second.")
        speak(weather_report)

    except Exception as e:
        print(f"Weather error: {e}")
        speak("Sorry, I couldn't fetch the weather right now.")


def shutdown_pc():
    """Shutdown the PC safely"""
    try:
        speak("Shutting down the computer in 10 seconds. Please save your work.")
        system_os = platform.system()

        if system_os == "Windows":
            os.system("shutdown /s /t 10")
        elif system_os in ["Linux", "Darwin"]:
            os.system("shutdown -h now")
        else:
            speak("Sorry, I cannot shutdown this operating system")
    except Exception as e:
        print(f"Shutdown error: {e}")
        speak("Sorry, I could not shutdown the PC")


def lock_pc():
    """Lock the PC"""
    try:
        system_os = platform.system()
        
        if system_os == "Windows":
            ctypes.windll.user32.LockWorkStation()
            speak("PC is now locked.")
        elif system_os == "Linux":
            os.system("gnome-screensaver-command -l")
            speak("PC is now locked.")
        elif system_os == "Darwin":
            os.system("/System/Library/CoreServices/Menu\\ Extras/User.menu/Contents/Resources/CGSession -suspend")
            speak("Mac is now locked.")
        else:
            speak("Sorry, I cannot lock this operating system.")
    except Exception as e:
        print(f"Lock PC error: {e}")
        speak("Sorry, I could not lock the PC.")


def take_screenshot():
    """Take a screenshot and save it"""
    try:
        screenshots_dir = Path.home() / "Pictures" / "Screenshots"
        screenshots_dir.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = screenshots_dir / f"screenshot_{timestamp}.png"
        
        screenshot = pyautogui.screenshot()
        screenshot.save(str(filename))
        
        speak(f"Screenshot saved successfully")
    except Exception as e:
        print(f"Screenshot error: {e}")
        speak("Sorry, I could not take the screenshot.")


def get_volume_interface():
    """Get volume control interface (Windows only)"""
    try:
        from ctypes import cast, POINTER
        from comtypes import CLSCTX_ALL
        from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
        
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = cast(interface, POINTER(IAudioEndpointVolume))
        return volume
    except Exception as e:
        print(f"Volume interface error: {e}")
        return None


def increase_volume():
    """Increase system volume by 10%"""
    try:
        volume = get_volume_interface()
        if volume:
            current = volume.GetMasterVolumeLevelScalar()
            new = min(current + 0.1, 1.0)
            volume.SetMasterVolumeLevelScalar(new, None)
            speak(f"Volume increased to {int(new*100)} percent")
        else:
            speak("Volume control not available")
    except Exception as e:
        print(f"Increase volume error: {e}")
        speak("Sorry, I could not increase the volume.")


def decrease_volume():
    """Decrease system volume by 10%"""
    try:
        volume = get_volume_interface()
        if volume:
            current = volume.GetMasterVolumeLevelScalar()
            new = max(current - 0.1, 0.0)
            volume.SetMasterVolumeLevelScalar(new, None)
            speak(f"Volume decreased to {int(new*100)} percent")
        else:
            speak("Volume control not available")
    except Exception as e:
        print(f"Decrease volume error: {e}")
        speak("Sorry, I could not decrease the volume.")


def mute_volume():
    """Mute system volume"""
    try:
        volume = get_volume_interface()
        if volume:
            volume.SetMute(1, None)
            speak("Volume muted")
        else:
            speak("Volume control not available")
    except Exception as e:
        print(f"Mute volume error: {e}")
        speak("Sorry, I could not mute the volume.")


def check_internet_speed():
    """Check internet speed"""
    try:
        speak("Checking internet speed. This may take a few seconds.")
        st = speedtest.Speedtest()
        st.get_best_server()
        download_speed = st.download() / 1_000_000
        upload_speed = st.upload() / 1_000_000
        ping = st.results.ping

        speak(f"Download speed: {download_speed:.2f} megabits per second. "
              f"Upload speed: {upload_speed:.2f} megabits per second. "
              f"Ping: {int(ping)} milliseconds.")
    except Exception as e:
        print(f"Internet speed error: {e}")
        speak("Sorry, I could not check the internet speed right now.")


def tell_time():
    """Speak the current time"""
    try:
        now = datetime.datetime.now()
        current_time = now.strftime("%I:%M %p")
        speak(f"The current time is {current_time}")
    except Exception as e:
        print(f"Tell time error: {e}")
        speak("Sorry, I could not tell the time right now.")


def tell_date():
    """Speak the current date"""
    try:
        now = datetime.datetime.now()
        current_date = now.strftime("%A, %d %B %Y")
        speak(f"Today's date is {current_date}")
    except Exception as e:
        print(f"Tell date error: {e}")
        speak("Sorry, I could not tell the date right now.")


def create_note(text):
    """Create a note with the given text"""
    try:
        notes_folder = Path.home() / "Documents" / "AssistantNotes"
        notes_folder.mkdir(parents=True, exist_ok=True)

        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = notes_folder / f"note_{timestamp}.txt"

        filename.write_text(text, encoding="utf-8")
        speak("Note saved successfully")
    except Exception as e:
        print(f"Create note error: {e}")
        speak("Sorry, I could not create the note.")


def create_folder(folder_name):
    """Create a folder in the Documents directory"""
    try:
        base_path = Path.home() / "Documents"
        folder_path = base_path / folder_name

        if not folder_path.exists():
            folder_path.mkdir(parents=True)
            speak(f"Folder {folder_name} created successfully in Documents.")
        else:
            speak(f"Folder {folder_name} already exists in Documents.")
    except Exception as e:
        print(f"Create folder error: {e}")
        speak("Sorry, I could not create the folder.")


def delete_file(file_path):
    """Delete a file at the given path"""
    try:
        path = Path(file_path)
        if path.exists():
            path.unlink()
            speak(f"File {path.name} has been deleted successfully.")
        else:
            speak("Sorry, the file does not exist.")
    except Exception as e:
        print(f"Delete file error: {e}")
        speak("Sorry, I could not delete the file.")


def check_battery_status():
    """Check and speak battery status"""
    try:
        battery = psutil.sensors_battery()
        if battery:
            percent = battery.percent
            plugged = battery.power_plugged
            status = "charging" if plugged else "not charging"
            speak(f"The battery is at {int(percent)} percent and is currently {status}.")
        else:
            speak("Sorry, I could not detect battery information.")
    except Exception as e:
        print(f"Battery status error: {e}")
        speak("Sorry, I could not check the battery status.")


def sleepthepc():
    """Put the PC to sleep"""
    try:
        speak("Putting the computer to sleep.")
        if platform.system() == "Windows":
            os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
        else:
            speak("Sleep function not available for this operating system")
    except Exception as e:
        print(f"Sleep PC error: {e}")
        speak("Sorry, I could not put the PC to sleep.")


def empty_recycle_bin():
    """Empty the Windows Recycle Bin"""
    try:
        if platform.system() != "Windows":
            speak("This feature is only available on Windows")
            return
            
        speak("Are you sure you want to empty the Recycle Bin? Please say yes or no.")
        confirmation = takecommand()
        
        if "yes" in confirmation:
            winshell.recycle_bin().empty(confirm=False, show_progress=True, sound=True)
            speak("Recycle Bin has been emptied successfully.")
        else:
            speak("Okay, Recycle Bin not emptied.")
            
    except Exception as e:
        print(f"Empty Recycle Bin error: {e}")
        speak("Sorry, I could not empty the Recycle Bin.")


def search_wikipedia(topic):
    """Search Wikipedia for a topic"""
    try:
        speak(f"Searching Wikipedia for {topic}")
        wikipedia.set_lang("en")
        summary = wikipedia.summary(topic, sentences=3)
        speak(summary)
    except wikipedia.DisambiguationError:
        speak("There are multiple results for this topic. Please be more specific.")
    except wikipedia.PageError:
        speak("Sorry, I could not find any information on that topic.")
    except Exception as e:
        print(f"Wikipedia search error: {e}")
        speak("Sorry, I could not fetch Wikipedia information.")


def add_task(task):
    """Add a task to the to-do list"""
    try:
        with open(TODO_FILE, "a", encoding="utf-8") as f:
            f.write(task + "\n")
        speak(f"Task added: {task}")
    except Exception as e:
        print(f"Add task error: {e}")
        speak("Sorry, I could not add the task.")


def show_tasks():
    """Show all tasks"""
    try:
        if os.path.exists(TODO_FILE):
            with open(TODO_FILE, "r", encoding="utf-8") as f:
                tasks = f.readlines()
            if tasks:
                speak("Here are your tasks:")
                for i, task in enumerate(tasks, start=1):
                    speak(f"{i}. {task.strip()}")
            else:
                speak("Your to-do list is empty.")
        else:
            speak("Your to-do list is empty.")
    except Exception as e:
        print(f"Show tasks error: {e}")
        speak("Sorry, I could not read your tasks.")


def delete_task(task_number):
    """Delete a task by its number"""
    try:
        if os.path.exists(TODO_FILE):
            with open(TODO_FILE, "r", encoding="utf-8") as f:
                tasks = f.readlines()
            if 1 <= task_number <= len(tasks):
                removed_task = tasks.pop(task_number - 1)
                with open(TODO_FILE, "w", encoding="utf-8") as f:
                    f.writelines(tasks)
                speak(f"Removed task: {removed_task.strip()}")
            else:
                speak("Invalid task number.")
        else:
            speak("Your to-do list is empty.")
    except Exception as e:
        print(f"Delete task error: {e}")
        speak("Sorry, I could not delete the task.")


def set_reminder(task, time_str):
    """Set a reminder"""
    try:
        reminder_time = datetime.datetime.strptime(time_str, "%H:%M")
        now = datetime.datetime.now()
        reminder_datetime = now.replace(hour=reminder_time.hour, minute=reminder_time.minute, second=0)
        
        if reminder_datetime < now:
            reminder_datetime += datetime.timedelta(days=1)
            
        reminders.append((task, reminder_datetime))
        speak(f"Reminder set for {task} at {time_str}")
    except Exception as e:
        print(f"Set reminder error: {e}")
        speak("Sorry, I could not set the reminder. Please use HH:MM format like 14:30")


def reminder_checker():
    """Background thread to check reminders"""
    while True:
        now = datetime.datetime.now()
        for reminder in reminders[:]:
            task, reminder_time = reminder
            if now >= reminder_time:
                speak(f"Reminder: {task}")
                reminders.remove(reminder)
        time.sleep(30)

def check_disk_usage(drive_letter="C"):
    """Check disk usage for a given drive"""
    try:
        drive_letter = drive_letter.strip().lower()

        # 🔥 Map speech variations to proper drive letters
        drive_letter_map = {
            "see": "C",
            "sea": "C",
            "c": "C",
            "c drive": "C",
            "d": "D",
            "dee": "D",
            "d drive": "D",
            "e": "E",
            "ee": "E",
            "e drive": "E"
        }

        # Replace with mapped letter (default to uppercase input)
        drive_letter = drive_letter_map.get(drive_letter, drive_letter.upper())

        if len(drive_letter) == 1 and drive_letter in string.ascii_uppercase:
            drive_path = f"{drive_letter}:\\"

            if platform.system() != "Windows":
                speak("Disk usage check is currently only available on Windows")
                return

            partitions = [p.device.upper() for p in psutil.disk_partitions()]
            if drive_path not in partitions:
                speak(f"Drive {drive_letter} is not available.")
                return

            total, used, free = shutil.disk_usage(drive_path)
            total_gb = total // (2**30)
            used_gb = used // (2**30)
            free_gb = free // (2**30)

            speak(
                f"Disk usage for drive {drive_letter}: "
                f"Total {total_gb} gigabytes, "
                f"Used {used_gb} gigabytes, "
                f"Free {free_gb} gigabytes"
            )
        else:
            speak("Invalid drive letter. Please say a valid drive like C or D")
    except Exception as e:
        print(f"Disk usage error: {e}")
        speak("Sorry, I could not check disk usage.")



def check_system_usage():
    """Check CPU and RAM usage"""
    try:
        cpu_percent = psutil.cpu_percent(interval=1)  # CPU usage %
        memory = psutil.virtual_memory()  # RAM stats
        ram_percent = memory.percent
        total_ram_gb = round(memory.total / (1024**3), 2)
        available_ram_gb = round(memory.available / (1024**3), 2)

        result = (
            f"CPU usage is at {cpu_percent} percent. "
            f"RAM usage is at {ram_percent} percent. "
            f"Total RAM {total_ram_gb} gigabytes, "
            f"Available {available_ram_gb} gigabytes."
        )
        print(result)
        speak(result)
    except Exception as e:
        print(f"System usage error: {e}")
        speak("Sorry, I could not check system usage right now.")



@eel.expose
def allCommands(message=1):
    """Main command processor"""
    global CURRENT_LANGUAGE, CURRENT_LANG_CODE
    
    if message == 1:
        query = takecommand()
        print(query)
        eel.senderText(query)
    else:
        query = message
        eel.senderText(query)
    
    if not query or not query.strip():
        return
    
    try:
        # Language commands
        if "change language" in query or "switch language" in query:
            speak("Which language would you like?")
            lang_query = takecommand()
            
            for lang_name in LANGUAGES.keys():
                if lang_name in lang_query:
                    change_language(lang_name)
                    return
            
            speak("Language not recognized. Please try again")
        
        elif "list languages" in query or "available languages" in query:
            list_available_languages()
        
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
        
        # System commands
        elif "open" in query or "launch" in query or "start" in query:
            from engine.features import openCommand
            openCommand(query)
        
        elif "on youtube" in query:
            from engine.features import PlayYoutube
            PlayYoutube(query)
        
        elif "weather" in query:
            speak("Please tell me the city name")
            city_name = takecommand()
            if city_name:
                get_weather(city_name)
            else:
                speak("City name not recognized")
        
        elif "shutdown" in query or "turn off" in query:
            shutdown_pc()
        
        elif "lock" in query:
            lock_pc()
        
        elif "screenshot" in query or "capture screen" in query:
            take_screenshot()
        
        elif "increase volume" in query:
            increase_volume()
        
        elif "decrease volume" in query:
            decrease_volume()
        
        elif "mute" in query:
            mute_volume()
        
        elif "internet speed" in query or "speed test" in query:
            check_internet_speed()
        
        elif "time" in query and "current" in query:
            tell_time()
        
        elif "date" in query and ("current" in query or "today" in query):
            tell_date()
        
        elif "create note" in query or "take note" in query:
            speak("What would you like me to write in the note?")
            note_text = takecommand()
            if note_text:
                create_note(note_text)
            else:
                speak("Note text not recognized")
        
        elif "create folder" in query or "make folder" in query:
            speak("What should be the folder name?")
            folder_name = takecommand()
            if folder_name:
                create_folder(folder_name)
            else:
                speak("Folder name not recognized")
        
        elif "delete file" in query or "remove file" in query:
            speak("Please tell me the full path of the file to delete")
            file_path = takecommand()
            file_path = file_path.replace(" slash ", "/").replace(" backslash ", "\\")
            if file_path:
                delete_file(file_path)
            else:
                speak("File path not recognized")
        
        elif "battery" in query:
            check_battery_status()
        
        elif "sleep" in query and "pc" in query:
            sleepthepc()
        
        elif "empty recycle bin" in query or "clear recycle bin" in query:
            empty_recycle_bin()
        
        elif "wikipedia" in query or "search wikipedia" in query:
            speak("What topic should I search for?")
            topic = takecommand()
            if topic:
                search_wikipedia(topic)
            else:
                speak("Topic not recognized.")
        
        elif "add task" in query or "add to-do" in query:
            speak("What task would you like to add?")
            task = takecommand()
            if task:
                add_task(task)
            else:
                speak("Task not recognized.")
        
        elif "show tasks" in query or "read tasks" in query or "my tasks" in query:
            show_tasks()
        
        elif "delete task" in query or "remove task" in query:
            speak("Please tell me the task number to remove")
            task_number_text = takecommand()
            try:
                task_number = int(task_number_text)
                delete_task(task_number)
            except ValueError:
                speak("Invalid task number. Please say a number.")
        
        elif "set reminder" in query or "remind me" in query:
            speak("What should I remind you about?")
            task = takecommand()
            speak("At what time? Please say in HH:MM 24-hour format")
            time_str = takecommand()
            time_str = time_str.replace(" ", "").replace(".", ":")
            set_reminder(task, time_str)
        
        elif "disk usage" in query or "disk space" in query or "free space" in query:
            speak("Which drive would you like me to check?")
            drive_letter = takecommand().strip().lower()
            drive_map = {"see": "C", "sea": "C", "c": "C", "d": "D", "dee": "D"}
            drive = drive_map.get(drive_letter, drive_letter.upper())
            check_disk_usage(drive)
        elif "check cpu" in query or "cpu usage" in query or "ram usage" in query or "system usage" in query:
            check_system_usage()

        elif "send message" in query or "phone call" in query or "video call" in query:
            from engine.features import findContact, whatsApp, makeCall, sendMessage
            contact_no, name = findContact(query)
            
            if contact_no != 0:
                speak("Which mode you want to use whatsapp or mobile")
                preference = takecommand()

                if "mobile" in preference:
                    if "send message" in query or "send sms" in query: 
                        speak("What message to send")
                        message = takecommand()
                        sendMessage(message, contact_no, name)
                    elif "phone call" in query:
                        makeCall(name, contact_no)
                    else:
                        speak("Please try again")
                
                elif "whatsapp" in preference:
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
        try:
            audio = r.listen(source, timeout=5, phrase_time_limit=3)
            query = r.recognize_google(audio, language='en-in')
            if "ira" in query.lower():
                speak("Yes, I'm listening")
                allCommands()
        except:
            pass


def initialize():
    """Initialize the assistant"""
    print("Initializing Multi-Language Voice Assistant...")
    speak("Voice assistant initialized and ready")
    print(f"Current language: {CURRENT_LANGUAGE}")
    print("Say 'change language' to switch languages")
    
    # Start reminder checker thread
    reminder_thread = threading.Thread(target=reminder_checker, daemon=True)
    reminder_thread.start()


if __name__ == "__main__":
    initialize()