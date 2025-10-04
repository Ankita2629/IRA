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
import PyPDF2
import screen_brightness_control as sbc

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
def restartthepc():
    """Restart the PC safely"""
    try:
        speak("Restarting the computer in 10 seconds. Please save your work.")
        system_os = platform.system()

        if system_os == "Windows":
            os.system("shutdown /r /t 10")
        elif system_os in ["Linux", "Darwin"]:
            os.system("shutdown -r now")
        else:
            speak("Sorry, I cannot restart this operating system")
    except Exception as e:
        print(f"Restart error: {e}")
        speak("Sorry, I could not restart the PC")

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
def adjust_brightness(command):
    """Adjust screen brightness based on voice command."""
    current = sbc.get_brightness(display=0)[0]  # Get current brightness
    if "increase brightness" in command:
        new_brightness = min(current + 10, 100)  # Increase by 10%, max 100%
        sbc.set_brightness(new_brightness)
        speak(f"Brightness increased to {new_brightness}%")
    elif "decrease brightness" in command:
        new_brightness = max(current - 10, 0)  # Decrease by 10%, min 0%
        sbc.set_brightness(new_brightness)
        speak(f"Brightness decreased to {new_brightness}%")
    elif "set brightness" in command:
        # Example: "set brightness to 70"
        try:
            value = int(command.split("to")[-1].strip())
            value = max(0, min(value, 100))
            sbc.set_brightness(value)
            speak(f"Brightness set to {value}%")
        except:
            speak("Sorry, I couldn't understand the brightness value.")

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
def get_wifi_info():
    """Get Wi-Fi network information"""
    try:
        system_os = platform.system()
        
        if system_os == "Windows":
            # Get connected Wi-Fi name
            result = os.popen('netsh wlan show interfaces').read()
            
            if "disconnected" in result.lower() or "SSID" not in result:
                speak("You are not connected to any Wi-Fi network")
                return
            
            # Extract SSID (network name)
            ssid = None
            signal = None
            for line in result.split('\n'):
                if "SSID" in line and "BSSID" not in line:
                    ssid = line.split(":")[1].strip()
                elif "Signal" in line:
                    signal = line.split(":")[1].strip()
            
            if ssid:
                info = f"You are connected to {ssid}"
                if signal:
                    info += f" with signal strength {signal}"
                speak(info)
            else:
                speak("Could not retrieve Wi-Fi information")
                
        elif system_os == "Linux":
            # For Linux systems
            result = os.popen('iwgetid -r').read().strip()
            if result:
                speak(f"You are connected to {result}")
            else:
                speak("You are not connected to any Wi-Fi network")
                
        elif system_os == "Darwin":  # macOS
            result = os.popen('/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport -I | grep " SSID"').read()
            if result:
                ssid = result.split(":")[1].strip()
                speak(f"You are connected to {ssid}")
            else:
                speak("You are not connected to any Wi-Fi network")
        else:
            speak("Wi-Fi info not available for this operating system")
            
    except Exception as e:
        print(f"Wi-Fi info error: {e}")
        speak("Sorry, I could not retrieve Wi-Fi information")


def get_network_info():
    """Get detailed network information including IP addresses"""
    try:
        # Get all network interfaces
        addrs = psutil.net_if_addrs()
        stats = psutil.net_if_stats()
        
        active_networks = []
        
        for interface_name, interface_addresses in addrs.items():
            # Check if interface is up
            if interface_name in stats and stats[interface_name].isup:
                for address in interface_addresses:
                    # IPv4 address
                    if str(address.family) == 'AddressFamily.AF_INET':
                        active_networks.append({
                            'interface': interface_name,
                            'ip': address.address,
                            'netmask': address.netmask
                        })
        
        if active_networks:
            speak("Here is your network information:")
            for network in active_networks:
                # Skip loopback
                if network['ip'] != '127.0.0.1':
                    speak(f"Interface {network['interface']}: IP address {network['ip']}")
        else:
            speak("No active network connections found")
            
    except Exception as e:
        print(f"Network info error: {e}")
        speak("Sorry, I could not retrieve network information")


def show_wifi_password(network_name=None):
    """Show saved Wi-Fi password (Windows only)"""
    try:
        if platform.system() != "Windows":
            speak("This feature is only available on Windows")
            return
        
        if not network_name:
            # Get current network
            result = os.popen('netsh wlan show interfaces').read()
            for line in result.split('\n'):
                if "SSID" in line and "BSSID" not in line:
                    network_name = line.split(":")[1].strip()
                    break
        
        if not network_name:
            speak("Could not determine the network name")
            return
        
        # Get password
        command = f'netsh wlan show profile name="{network_name}" key=clear'
        result = os.popen(command).read()
        
        password = None
        for line in result.split('\n'):
            if "Key Content" in line:
                password = line.split(":")[1].strip()
                break
        
        if password:
            speak(f"The password for {network_name} is {password}")
            print(f"Password: {password}")  # Also print for security
        else:
            speak(f"Could not retrieve password for {network_name}. You may not have saved this network.")
            
    except Exception as e:
        print(f"Wi-Fi password error: {e}")
        speak("Sorry, I could not retrieve the Wi-Fi password")


def list_available_wifi():
    """List all available Wi-Fi networks"""
    try:
        if platform.system() == "Windows":
            speak("Scanning for available Wi-Fi networks. Please wait.")
            result = os.popen('netsh wlan show networks mode=bssid').read()
            
            networks = []
            for line in result.split('\n'):
                if "SSID" in line and "BSSID" not in line:
                    ssid = line.split(":")[1].strip()
                    if ssid and ssid != "":
                        networks.append(ssid)
            
            if networks:
                speak(f"Found {len(networks)} networks:")
                for i, network in enumerate(networks[:5], 1):  # Limit to first 5
                    speak(f"{i}. {network}")
                if len(networks) > 5:
                    speak(f"And {len(networks) - 5} more networks")
            else:
                speak("No Wi-Fi networks found")
        else:
            speak("This feature is currently only available on Windows")
            
    except Exception as e:
        print(f"List Wi-Fi error: {e}")
        speak("Sorry, I could not scan for Wi-Fi networks")
def read_text_file(file_path):
    """Read a .txt file and speak its contents"""
    try:
        if not os.path.exists(file_path):
            speak("The specified text file does not exist.")
            return
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read().strip()
        if content:
            speak("Reading text file content now.")
            for chunk in [content[i:i+3000] for i in range(0, len(content), 3000)]:
                speak(chunk)
        else:
            speak("The text file is empty.")
    except Exception as e:
        print(f"Text file read error: {e}")
        speak("Sorry, I could not read the text file.")

def read_pdf_file(file_path, start_page=0, end_page=None):
    """Read a PDF file aloud using PyPDF2"""
    try:
        if not os.path.exists(file_path):
            speak("The specified PDF file does not exist.")
            return
        with open(file_path, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            num_pages = len(reader.pages)
            if end_page is None or end_page > num_pages:
                end_page = num_pages
            if start_page < 0 or start_page >= num_pages:
                speak("Invalid starting page number.")
                return
            speak(f"Reading PDF from page {start_page+1} to {end_page}")
            for i in range(start_page, end_page):
                try:
                    text = reader.pages[i].extract_text()
                    if text and text.strip():
                        for chunk in [text[j:j+3000] for j in range(0, len(text), 3000)]:
                            speak(chunk)
                    else:
                        speak(f"Page {i+1} has no readable text.")
                except Exception as e:
                    print(f"Error reading page {i+1}: {e}")
                    speak(f"Could not read page {i+1}.")
    except Exception as e:
        print(f"PDF read error: {e}")
        speak("Sorry, I could not read the PDF file.")

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
        elif "restart" in query or "reboot" in query:
            restartthepc()
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
        elif "increase brightness" in query or "decrease brightness" in query or "set brightness" in query:
            adjust_brightness(query)
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
        elif "wifi info" in query or "wi-fi info" in query or "network name" in query:
            get_wifi_info()
        
        elif "network info" in query or "ip address" in query or "my ip" in query:
            get_network_info()
        
        elif "wifi password" in query or "wi-fi password" in query or "network password" in query:
            if "current" in query or "this" in query:
                show_wifi_password()
            else:
                speak("Which network password would you like?")
                network_name = takecommand()
                if network_name:
                    show_wifi_password(network_name)
        
        elif "scan wifi" in query or "available networks" in query or "list networks" in query:
            list_available_wifi()
        elif "who are you" in query or "what is your name" in query or "your name" in query:
            speak("I am IRA, your intelligent voice assistant. I'm here to help you with various tasks.")
        
        elif "who created you" in query or "who made you" in query or "your creator" in query or "who developed you" in query:
            speak("I was created by Ankita, Anjali, Shubham and Amrita.")
        
        elif "who is your creator" in query or "who is your developer" in query:
            speak("My creators are Ankita, Anjali, Shubham and Amrita. They developed me to assist you.")
        
        elif "tell me about yourself" in query or "introduce yourself" in query:
            speak("Hello! I am IRA, an intelligent voice assistant created by Ankita, Anjali, Shubham and Amrita. I can help you with many tasks like checking weather, managing files, controlling your system, and much more. Just ask me anything!")
        elif "what is unique" in query or "what makes you different" in query or "what makes you special" in query or "your uniqueness" in query or "why choose you" in query:
            speak("What makes me unique is my multilingual capability. I can speak and understand over 27 languages including English, Hindi, Spanish, French, German, Tamil, Telugu, Bengali, Arabic, Chinese, Japanese, Korean, and many more. "
                  "You can seamlessly switch between languages anytime. I also offer comprehensive system control, including Wi-Fi management, disk usage monitoring, battery status, volume control, screenshot capture, and even reveal Wi-Fi passwords. "
                  "Plus, I have built-in task management, reminders, note-taking, Wikipedia search, weather updates, and internet speed testing. "
                  "I'm designed to be your complete personal assistant with the power of multiple languages at your command.")
        elif "read pdf" in query:
            speak("Which file should I read?")
            file_name = takecommand()
            if file_name:
              try:
                read_pdf_file(file_name)
              except Exception:
                speak("I could not open that PDF file.")

        elif "read text" in query or "read note" in query:
          speak("Which text file should I read?")
          file_name = takecommand()
          if file_name:
             try:
               read_text_file(file_name)
             except Exception:
               speak("I could not open that text file.")

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
    """Listen for wake word 'IRA'"""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening for 'IRA'...")
        r.adjust_for_ambient_noise(source, duration=0.5)
        
        try:
            audio = r.listen(source, timeout=None, phrase_time_limit=3)
            query = r.recognize_google(audio, language='en-in').lower()
            print(f"Heard: {query}")
            
            if "ira" in query:
                print("✓ Wake word detected!")
                speak("Yes, how can I help?")
                allCommands()
                
        except sr.UnknownValueError:
            # Couldn't understand audio - this is normal, just continue
            pass
        except sr.RequestError as e:
            print(f"Speech recognition service error: {e}")
            time.sleep(2)
        except Exception as e:
            print(f"Hotword error: {e}")
            time.sleep(1)

def start_hotword_thread():
    """Run hotword detection in background"""
    while True:
        try:
            hotword_listener()
        except Exception as e:
            print(f"Hotword thread error: {e}")
            time.sleep(1)


def initialize():
    """Initialize the assistant"""
    print("Initializing Multi-Language Voice Assistant...")
    speak("Voice assistant initialized and ready")
    print(f"Current language: {CURRENT_LANGUAGE}")
    print("Say 'IRA' to activate voice commands")
    
    # Start reminder checker thread
    reminder_thread = threading.Thread(target=reminder_checker, daemon=True)
    reminder_thread.start()
    
    # Start hotword listener thread
    hotword_thread = threading.Thread(target=start_hotword_thread, daemon=True)
    hotword_thread.start()


if __name__ == "__main__":
    initialize()
    
    # Start Eel web interface
    eel.init("web")  # Change "web" to your actual web folder name
    eel.start("index.html", mode='chrome', size=(1000, 600), port=8080)
import base64
import PyPDF2
from setuptools import sic
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
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
import google.generativeai as genai
import json
import re

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
GEMINI_API_KEY = "AIzaSyCYDb08-0XuFyK4s5EGzmmtsyieG_PjW1g"
genai.configure(api_key=GEMINI_API_KEY)

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
def restartthepc():
    """Restart the PC safely"""
    try:
        speak("Restarting the computer in 10 seconds. Please save your work.")
        system_os = platform.system()

        if system_os == "Windows":
            os.system("shutdown /r /t 10")
        elif system_os in ["Linux", "Darwin"]:
            os.system("shutdown -r now")
        else:
            speak("Sorry, I cannot restart this operating system")
    except Exception as e:
        print(f"Restart error: {e}")
        speak("Sorry, I could not restart the PC")

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
def adjust_brightness(command):
    """Adjust screen brightness based on voice command."""
    current = sic.get_brightness(display=0)[0]  # Get current brightness
    if "increase brightness" in command:
        new_brightness = min(current + 10, 100)  # Increase by 10%, max 100%
        sic.set_brightness(new_brightness)
        speak(f"Brightness increased to {new_brightness}%")
    elif "decrease brightness" in command:
        new_brightness = max(current - 10, 0)  # Decrease by 10%, min 0%
        sic.set_brightness(new_brightness)
        speak(f"Brightness decreased to {new_brightness}%")
    elif "set brightness" in command:
        # Example: "set brightness to 70"
        try:
            value = int(command.split("to")[-1].strip())
            value = max(0, min(value, 100))
            sic.set_brightness(value)
            speak(f"Brightness set to {value}%")
        except:
            speak("Sorry, I couldn't understand the brightness value.")

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
def get_wifi_info():
    """Get Wi-Fi network information"""
    try:
        system_os = platform.system()
        
        if system_os == "Windows":
            # Get connected Wi-Fi name
            result = os.popen('netsh wlan show interfaces').read()
            
            if "disconnected" in result.lower() or "SSID" not in result:
                speak("You are not connected to any Wi-Fi network")
                return
            
            # Extract SSID (network name)
            ssid = None
            signal = None
            for line in result.split('\n'):
                if "SSID" in line and "BSSID" not in line:
                    ssid = line.split(":")[1].strip()
                elif "Signal" in line:
                    signal = line.split(":")[1].strip()
            
            if ssid:
                info = f"You are connected to {ssid}"
                if signal:
                    info += f" with signal strength {signal}"
                speak(info)
            else:
                speak("Could not retrieve Wi-Fi information")
                
        elif system_os == "Linux":
            # For Linux systems
            result = os.popen('iwgetid -r').read().strip()
            if result:
                speak(f"You are connected to {result}")
            else:
                speak("You are not connected to any Wi-Fi network")
                
        elif system_os == "Darwin":  # macOS
            result = os.popen('/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport -I | grep " SSID"').read()
            if result:
                ssid = result.split(":")[1].strip()
                speak(f"You are connected to {ssid}")
            else:
                speak("You are not connected to any Wi-Fi network")
        else:
            speak("Wi-Fi info not available for this operating system")
            
    except Exception as e:
        print(f"Wi-Fi info error: {e}")
        speak("Sorry, I could not retrieve Wi-Fi information")


def get_network_info():
    """Get detailed network information including IP addresses"""
    try:
        # Get all network interfaces
        addrs = psutil.net_if_addrs()
        stats = psutil.net_if_stats()
        
        active_networks = []
        
        for interface_name, interface_addresses in addrs.items():
            # Check if interface is up
            if interface_name in stats and stats[interface_name].isup:
                for address in interface_addresses:
                    # IPv4 address
                    if str(address.family) == 'AddressFamily.AF_INET':
                        active_networks.append({
                            'interface': interface_name,
                            'ip': address.address,
                            'netmask': address.netmask
                        })
        
        if active_networks:
            speak("Here is your network information:")
            for network in active_networks:
                # Skip loopback
                if network['ip'] != '127.0.0.1':
                    speak(f"Interface {network['interface']}: IP address {network['ip']}")
        else:
            speak("No active network connections found")
            
    except Exception as e:
        print(f"Network info error: {e}")
        speak("Sorry, I could not retrieve network information")


def show_wifi_password(network_name=None):
    """Show saved Wi-Fi password (Windows only)"""
    try:
        if platform.system() != "Windows":
            speak("This feature is only available on Windows")
            return
        
        if not network_name:
            # Get current network
            result = os.popen('netsh wlan show interfaces').read()
            for line in result.split('\n'):
                if "SSID" in line and "BSSID" not in line:
                    network_name = line.split(":")[1].strip()
                    break
        
        if not network_name:
            speak("Could not determine the network name")
            return
        
        # Get password
        command = f'netsh wlan show profile name="{network_name}" key=clear'
        result = os.popen(command).read()
        
        password = None
        for line in result.split('\n'):
            if "Key Content" in line:
                password = line.split(":")[1].strip()
                break
        
        if password:
            speak(f"The password for {network_name} is {password}")
            print(f"Password: {password}")  # Also print for security
        else:
            speak(f"Could not retrieve password for {network_name}. You may not have saved this network.")
            
    except Exception as e:
        print(f"Wi-Fi password error: {e}")
        speak("Sorry, I could not retrieve the Wi-Fi password")


def list_available_wifi():
    """List all available Wi-Fi networks"""
    try:
        if platform.system() == "Windows":
            speak("Scanning for available Wi-Fi networks. Please wait.")
            result = os.popen('netsh wlan show networks mode=bssid').read()
            
            networks = []
            for line in result.split('\n'):
                if "SSID" in line and "BSSID" not in line:
                    ssid = line.split(":")[1].strip()
                    if ssid and ssid != "":
                        networks.append(ssid)
            
            if networks:
                speak(f"Found {len(networks)} networks:")
                for i, network in enumerate(networks[:5], 1):  # Limit to first 5
                    speak(f"{i}. {network}")
                if len(networks) > 5:
                    speak(f"And {len(networks) - 5} more networks")
            else:
                speak("No Wi-Fi networks found")
        else:
            speak("This feature is currently only available on Windows")
            
    except Exception as e:
        print(f"List Wi-Fi error: {e}")
        speak("Sorry, I could not scan for Wi-Fi networks")

def generate_image_pollinations(prompt, width=1024, height=1024):
    """
    Generate image using Pollinations AI (Free, No API Key Required)
    """
    try:
        speak(f"Generating image: {prompt}. Please wait...")
        
        # Pollinations AI endpoint
        url = f"https://image.pollinations.ai/prompt/{requests.utils.quote(prompt)}"
        params = {
            "width": width,
            "height": height,
            "nologo": "true",
            "enhance": "true"
        }
        
        response = requests.get(url, params=params, timeout=60)
        
        if response.status_code == 200:
            # Create Images directory
            images_dir = Path.home() / "Pictures" / "IRA_Generated_Images"
            images_dir.mkdir(parents=True, exist_ok=True)
            
            # Save image
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            safe_prompt = "".join(c for c in prompt[:30] if c.isalnum() or c in (' ', '-', '_')).strip()
            filename = images_dir / f"{safe_prompt}_{timestamp}.png"
            
            with open(filename, 'wb') as f:
                f.write(response.content)
            
            speak(f"Image generated successfully and saved to Pictures folder")
            print(f"Image saved: {filename}")
            
            # Optional: Open the image
            try:
                import os
                os.startfile(str(filename))  # Windows
            except:
                pass
                
            return True
        else:
            speak("Failed to generate image. Please try again.")
            return False
            
    except Exception as e:
        print(f"Image generation error: {e}")
        speak("Sorry, I could not generate the image right now.")
        return False


def generate_image_stable_diffusion(prompt, api_key=None):
    """
    Generate image using Stability AI (Requires API Key)
    Get free API key from: https://platform.stability.ai/
    """
    try:
        if not api_key:
            speak("Stable Diffusion API key not configured")
            return False
        
        speak(f"Generating high-quality image: {prompt}. This may take a moment...")
        
        url = "https://api.stability.ai/v1/generation/stable-diffusion-xl-1024-v1-0/text-to-image"
        
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }
        
        data = {
            "text_prompts": [{"text": prompt}],
            "cfg_scale": 7,
            "height": 1024,
            "width": 1024,
            "samples": 1,
            "steps": 30,
        }
        
        response = requests.post(url, headers=headers, json=data, timeout=120)
        
        if response.status_code == 200:
            data = response.json()
            
            # Create Images directory
            images_dir = Path.home() / "Pictures" / "IRA_Generated_Images"
            images_dir.mkdir(parents=True, exist_ok=True)
            
            # Save image
            for i, image in enumerate(data["artifacts"]):
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                safe_prompt = "".join(c for c in prompt[:30] if c.isalnum() or c in (' ', '-', '_')).strip()
                filename = images_dir / f"{safe_prompt}_{timestamp}.png"
                
                img_data = base64.b64decode(image["base64"])
                with open(filename, 'wb') as f:
                    f.write(img_data)
                
                speak(f"High-quality image generated successfully")
                print(f"Image saved: {filename}")
                
                # Open the image
                try:
                    import os
                    os.startfile(str(filename))
                except:
                    pass
                    
            return True
        else:
            speak(f"Failed to generate image. Status: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"Stable Diffusion error: {e}")
        speak("Sorry, I could not generate the image with Stable Diffusion.")
        return False


def generate_image_huggingface(prompt, model="black-forest-labs/FLUX.1-schnell"):
    """
    Generate image using Hugging Face Inference API (Free)
    Default model: FLUX.1-schnell (Fast and free)
    """
    try:
        speak(f"Creating your image: {prompt}. Please wait...")
        
        API_URL = f"https://api-inference.huggingface.co/models/{model}"
        
        headers = {
            "Content-Type": "application/json",
        }
        
        payload = {
            "inputs": prompt,
        }
        
        response = requests.post(API_URL, headers=headers, json=payload, timeout=120)
        
        if response.status_code == 200:
            # Create Images directory
            images_dir = Path.home() / "Pictures" / "IRA_Generated_Images"
            images_dir.mkdir(parents=True, exist_ok=True)
            
            # Save image
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            safe_prompt = "".join(c for c in prompt[:30] if c.isalnum() or c in (' ', '-', '_')).strip()
            filename = images_dir / f"{safe_prompt}_{timestamp}.png"
            
            with open(filename, 'wb') as f:
                f.write(response.content)
            
            speak(f"Image created successfully and saved")
            print(f"Image saved: {filename}")
            
            # Open the image
            try:
                import os
                os.startfile(str(filename))
            except:
                pass
                
            return True
        else:
            speak("Image generation service is warming up. Please try again in a moment.")
            return False
            
    except Exception as e:
        print(f"Hugging Face generation error: {e}")
        speak("Sorry, I could not generate the image right now.")
        return False


# Main image generation function (uses free service by default)
def generate_image(prompt, service="pollinations", **kwargs):
    """
    Generate image using specified service
    
    Args:
        prompt: Text description of image to generate
        service: 'pollinations' (free, default), 'huggingface' (free), or 'stable-diffusion' (requires API key)
        **kwargs: Additional parameters (api_key for stable-diffusion, width, height, etc.)
    """
    if service == "pollinations":
        return generate_image_pollinations(prompt, 
                                          width=kwargs.get('width', 1024),
                                          height=kwargs.get('height', 1024))
    elif service == "huggingface":
        return generate_image_huggingface(prompt, 
                                         model=kwargs.get('model', 'black-forest-labs/FLUX.1-schnell'))
    elif service == "stable-diffusion":
        return generate_image_stable_diffusion(prompt, 
                                              api_key=kwargs.get('api_key'))
    else:
        speak("Unknown image generation service")
        return False

def generate_ppt_content_with_ai(topic, num_slides=7):
    """
    Generate PowerPoint content using Gemini AI
    """
    try:
        speak(f"Generating content for presentation on {topic}")
        
        # Configure the model
        model = genai.GenerativeModel('gemini-pro')
        
        prompt = f"""Create a PowerPoint presentation outline on "{topic}" with exactly {num_slides} slides.

Return ONLY valid JSON in this exact format (no markdown, no code blocks):
{{
    "title": "Main Presentation Title",
    "slides": [
        {{
            "title": "Slide 1 Title",
            "content": ["Bullet point 1", "Bullet point 2", "Bullet point 3"]
        }},
        {{
            "title": "Slide 2 Title", 
            "content": ["Point 1", "Point 2", "Point 3", "Point 4"]
        }}
    ]
}}

Requirements:
- First slide should be the title slide about "{topic}"
- Slides 2 to {num_slides-1} should have 3-5 informative bullet points each
- Last slide should be "Conclusion" or "Thank You"
- Make content specific, detailed and professional
- Return ONLY the JSON, nothing else"""

        response = model.generate_content(prompt)
        content_text = response.text.strip()
        
        # Clean up the response - remove markdown code blocks if present
        content_text = content_text.replace('```json', '').replace('```', '').strip()
        
        # Try to parse JSON
        try:
            content_data = json.loads(content_text)
            print(f"Successfully generated AI content with {len(content_data.get('slides', []))} slides")
            return content_data
        except json.JSONDecodeError as je:
            print(f"JSON parse error: {je}")
            # Try to extract JSON using regex
            json_match = re.search(r'\{[\s\S]*\}', content_text)
            if json_match:
                content_data = json.loads(json_match.group())
                return content_data
            raise
            
    except Exception as e:
        print(f"AI content generation error: {e}")
        speak("Using template content for presentation")
        
        # Fallback to template
        return {
            "title": topic,
            "slides": [
                {
                    "title": topic,
                    "content": [f"Overview of {topic}", "Key concepts and fundamentals", "Importance and relevance"]
                },
                {
                    "title": "Introduction",
                    "content": ["Background information", "Context and scope", "Objectives of this presentation"]
                },
                {
                    "title": "Main Points",
                    "content": ["First key point", "Second key point", "Third key point", "Supporting details"]
                },
                {
                    "title": "Analysis",
                    "content": ["In-depth examination", "Critical insights", "Data and evidence", "Expert perspectives"]
                },
                {
                    "title": "Applications",
                    "content": ["Practical uses", "Real-world examples", "Case studies", "Implementation strategies"]
                },
                {
                    "title": "Conclusion",
                    "content": ["Summary of key points", "Key takeaways", "Future implications", "Final thoughts"]
                },
                {
                    "title": "Thank You",
                    "content": ["Questions?", "Contact information", "Additional resources"]
                }
            ][:num_slides]
        }


def create_ppt_from_topic(topic, num_slides=7, design_theme="professional"):
    """
    Create PowerPoint from scratch based on topic using AI
    """
    try:
        speak(f"Creating presentation on {topic}. This may take a moment.")
        
        # Generate content using AI
        content_data = generate_ppt_content_with_ai(topic, num_slides)
        
        if not content_data or 'slides' not in content_data:
            speak("Failed to generate content properly")
            return False
        
        # Create presentation
        prs = Presentation()
        prs.slide_width = Inches(10)
        prs.slide_height = Inches(7.5)
        
        # Define color schemes
        themes = {
            "professional": {
                "bg": RGBColor(255, 255, 255),
                "title": RGBColor(0, 51, 102),
                "text": RGBColor(51, 51, 51),
                "accent": RGBColor(0, 112, 192)
            },
            "modern": {
                "bg": RGBColor(240, 240, 245),
                "title": RGBColor(51, 51, 51),
                "text": RGBColor(85, 85, 85),
                "accent": RGBColor(255, 87, 51)
            },
            "dark": {
                "bg": RGBColor(30, 30, 30),
                "title": RGBColor(255, 255, 255),
                "text": RGBColor(220, 220, 220),
                "accent": RGBColor(0, 200, 255)
            }
        }
        
        colors = themes.get(design_theme, themes["professional"])
        
        # Get slides data
        slides_data = content_data.get('slides', [])
        main_title = content_data.get('title', topic)
        
        # Title Slide
        title_slide_layout = prs.slide_layouts[0]
        slide = prs.slides.add_slide(title_slide_layout)
        
        title = slide.shapes.title
        subtitle = slide.placeholders[1]
        
        title.text = main_title
        subtitle.text = f"Generated by IRA\n{datetime.datetime.now().strftime('%B %d, %Y')}"
        
        # Style title
        if title.text_frame.paragraphs:
            title.text_frame.paragraphs[0].font.size = Pt(44)
            title.text_frame.paragraphs[0].font.bold = True
            title.text_frame.paragraphs[0].font.color.rgb = colors["title"]
        
        # Content Slides
        for idx, slide_data in enumerate(slides_data):
            if idx == 0:  # Skip first slide as it's usually a duplicate of title
                continue
                
            content_slide_layout = prs.slide_layouts[1]
            slide = prs.slides.add_slide(content_slide_layout)
            
            # Set title
            title_shape = slide.shapes.title
            slide_title = slide_data.get('title', f'Slide {idx + 1}')
            title_shape.text = slide_title
            
            if title_shape.text_frame.paragraphs:
                title_shape.text_frame.paragraphs[0].font.size = Pt(32)
                title_shape.text_frame.paragraphs[0].font.bold = True
                title_shape.text_frame.paragraphs[0].font.color.rgb = colors["title"]
            
            # Add content
            content = slide_data.get('content', [])
            if content and len(content) > 0:
                # Use the content placeholder
                body_shape = slide.placeholders[1]
                text_frame = body_shape.text_frame
                text_frame.clear()
                
                for i, point in enumerate(content):
                    if i == 0:
                        p = text_frame.paragraphs[0]
                    else:
                        p = text_frame.add_paragraph()
                    
                    p.text = str(point)
                    p.level = 0
                    p.font.size = Pt(18)
                    p.font.color.rgb = colors["text"]
                    p.space_before = Pt(8)
                    p.space_after = Pt(8)
        
        # Save presentation
        ppt_folder = Path.home() / "Documents" / "IRA_Presentations"
        ppt_folder.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        safe_topic = "".join(c for c in topic[:30] if c.isalnum() or c in (' ', '-', '_')).strip()
        filename = ppt_folder / f"{safe_topic}_{timestamp}.pptx"
        
        prs.save(str(filename))
        
        speak(f"Presentation on {topic} created successfully with {len(prs.slides)} slides")
        print(f"Saved: {filename}")
        
        # Open the file
        try:
            os.startfile(str(filename))
        except:
            pass
            
        return True
        
    except Exception as e:
        print(f"Create PPT error: {e}")
        import traceback
        traceback.print_exc()
        speak("Sorry, I encountered an error creating the presentation.")
        return False


def create_ppt_from_template(template_path, output_name, custom_data=None):
    """
    Create PowerPoint from existing template
    """
    try:
        prs = Presentation(template_path)
        
        # Modify template with custom data if provided
        if custom_data:
            if len(prs.slides) > 0:
                title_slide = prs.slides[0]
                if title_slide.shapes.title:
                    title_slide.shapes.title.text = custom_data.get('title', 'Presentation Title')
        
        # Save the presentation
        ppt_folder = Path.home() / "Documents" / "IRA_Presentations"
        ppt_folder.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = ppt_folder / f"{output_name}_{timestamp}.pptx"
        prs.save(str(filename))
        
        speak(f"Presentation created from template and saved successfully")
        print(f"Saved: {filename}")
        
        # Open the file
        try:
            os.startfile(str(filename))
        except:
            pass
            
        return True
        
    except Exception as e:
        print(f"Template PPT error: {e}")
        speak("Sorry, I could not create presentation from template")
        return False
def create_simple_ppt(title, slides_content):
    """
    Create a simple PowerPoint with provided content
    """
    try:
        prs = Presentation()
        
        # Title Slide
        title_slide_layout = prs.slide_layouts[0]
        slide = prs.slides.add_slide(title_slide_layout)
        slide.shapes.title.text = title
        slide.placeholders[1].text = f"Created by IRA\n{datetime.datetime.now().strftime('%B %d, %Y')}"
        
        # Content Slides
        for slide_info in slides_content:
            bullet_slide_layout = prs.slide_layouts[1]
            slide = prs.slides.add_slide(bullet_slide_layout)
            
            shapes = slide.shapes
            title_shape = shapes.title
            body_shape = shapes.placeholders[1]
            
            title_shape.text = slide_info['title']
            
            text_frame = body_shape.text_frame
            for point in slide_info['points']:
                p = text_frame.add_paragraph()
                p.text = point
                p.level = 0
        
        # Save
        ppt_folder = Path.home() / "Documents" / "IRA_Presentations"
        ppt_folder.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = ppt_folder / f"{title}_{timestamp}.pptx"
        prs.save(str(filename))
        
        speak("Simple presentation created successfully")
        
        try:
            import os
            os.startfile(str(filename))
        except:
            pass
            
        return True
        
    except Exception as e:
        print(f"Simple PPT error: {e}")
        speak("Could not create simple presentation")
        return False


def read_text_file(file_path):
    """Read a .txt file and speak its contents"""
    try:
        if not os.path.exists(file_path):
            speak("The specified text file does not exist.")
            return
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read().strip()
        if content:
            speak("Reading text file content now.")
            for chunk in [content[i:i+3000] for i in range(0, len(content), 3000)]:
                speak(chunk)
        else:
            speak("The text file is empty.")
    except Exception as e:
        print(f"Text file read error: {e}")
        speak("Sorry, I could not read the text file.")

def read_pdf_file(file_path, start_page=0, end_page=None):
    """Read a PDF file aloud using PyPDF2"""
    try:
        if not os.path.exists(file_path):
            speak("The specified PDF file does not exist.")
            return
        with open(file_path, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            num_pages = len(reader.pages)
            if end_page is None or end_page > num_pages:
                end_page = num_pages
            if start_page < 0 or start_page >= num_pages:
                speak("Invalid starting page number.")
                return
            speak(f"Reading PDF from page {start_page+1} to {end_page}")
            for i in range(start_page, end_page):
                try:
                    text = reader.pages[i].extract_text()
                    if text and text.strip():
                        for chunk in [text[j:j+3000] for j in range(0, len(text), 3000)]:
                            speak(chunk)
                    else:
                        speak(f"Page {i+1} has no readable text.")
                except Exception as e:
                    print(f"Error reading page {i+1}: {e}")
                    speak(f"Could not read page {i+1}.")
    except Exception as e:
        print(f"PDF read error: {e}")
        speak("Sorry, I could not read the PDF file.")

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
        elif "restart" in query or "reboot" in query:
            restartthepc()
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
        elif "increase brightness" in query or "decrease brightness" in query or "set brightness" in query:
            adjust_brightness(query)
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
        elif "wifi info" in query or "wi-fi info" in query or "network name" in query:
            get_wifi_info()
        
        elif "network info" in query or "ip address" in query or "my ip" in query:
            get_network_info()
        
        elif "wifi password" in query or "wi-fi password" in query or "network password" in query:
            if "current" in query or "this" in query:
                show_wifi_password()
            else:
                speak("Which network password would you like?")
                network_name = takecommand()
                if network_name:
                    show_wifi_password(network_name)
        
        elif "scan wifi" in query or "available networks" in query or "list networks" in query:
            list_available_wifi()
        elif "who are you" in query or "what is your name" in query or "your name" in query:
            speak("I am IRA, your intelligent voice assistant. I'm here to help you with various tasks.")
        
        elif "who created you" in query or "who made you" in query or "your creator" in query or "who developed you" in query:
            speak("I was created by Ankita, Anjali, Shubham and Amrita.")
        
        elif "who is your creator" in query or "who is your developer" in query:
            speak("My creators are Ankita, Anjali, Shubham and Amrita. They developed me to assist you.")
        
        elif "tell me about yourself" in query or "introduce yourself" in query:
            speak("Hello! I am IRA, an intelligent voice assistant created by Ankita, Anjali, Shubham and Amrita. I can help you with many tasks like checking weather, managing files, controlling your system, and much more. Just ask me anything!")
        elif "what is unique" in query or "what makes you different" in query or "what makes you special" in query or "your uniqueness" in query or "why choose you" in query:
            speak("What makes me unique is my multilingual capability. I can speak and understand over 27 languages including English, Hindi, Spanish, French, German, Tamil, Telugu, Bengali, Arabic, Chinese, Japanese, Korean, and many more. "
                  "You can seamlessly switch between languages anytime. I also offer comprehensive system control, including Wi-Fi management, disk usage monitoring, battery status, volume control, screenshot capture, and even reveal Wi-Fi passwords. "
                  "Plus, I have built-in task management, reminders, note-taking, Wikipedia search, weather updates, and internet speed testing. "
                  "I'm designed to be your complete personal assistant with the power of multiple languages at your command.")
        elif "read pdf" in query:
            speak("Which file should I read?")
            file_name = takecommand()
            if file_name:
              try:
                read_pdf_file(file_name)
              except Exception:
                speak("I could not open that PDF file.")

        elif "read text" in query or "read note" in query:
          speak("Which text file should I read?")
          file_name = takecommand()
          if file_name:
             try:
               read_text_file(file_name)
             except Exception:
               speak("I could not open that text file.")

        elif "generate image" in query or "create image" in query or "draw image" in query or "make image" in query:
            speak("What image would you like me to generate? Please describe it in detail.")
            image_prompt = takecommand()
    
            if image_prompt:
                generate_image(image_prompt, service="pollinations")
            else:
                speak("I didn't catch the image description. Please try again.")

        elif "generate photo" in query or "create picture" in query or "make picture" in query:
            speak("Please describe the photo you want me to create")
            image_prompt = takecommand()
    
            if image_prompt:
                generate_image(image_prompt, service="pollinations")
            else:
                speak("Image description not recognized.")

        # PowerPoint Generation Commands
        elif "create presentation" in query or "make presentation" in query or "create ppt" in query or "make ppt" in query:
            speak("Would you like to create from a template or from a topic?")
            choice = takecommand()
            
            if "template" in choice:
                speak("Please provide the full path to your template file")
                template_path = takecommand()
                speak("What should be the presentation name?")
                ppt_name = takecommand()
                
                if template_path and ppt_name:
                    create_ppt_from_template(template_path, ppt_name)
                else:
                    speak("Template path or name not recognized")
            
            elif "topic" in choice:
                speak("What topic should the presentation be about?")
                topic = takecommand()
                
                if topic:
                    speak("How many slides would you like? Say a number between 5 and 15")
                    num_slides_text = takecommand()
                    
                    try:
                        num_slides = int(''.join(filter(str.isdigit, num_slides_text)))
                        num_slides = max(5, min(num_slides, 15))
                    except:
                        num_slides = 7
                        speak("Using default 7 slides")
                    
                    speak("Which design theme? Professional, modern, or dark?")
                    theme_choice = takecommand()
                    theme = "professional"
                    if "modern" in theme_choice:
                        theme = "modern"
                    elif "dark" in theme_choice:
                        theme = "dark"
                    
                    create_ppt_from_topic(topic, num_slides, theme)
                else:
                    speak("Topic not recognized")
            else:
                speak("Please specify template or topic")
        
        elif "presentation on" in query or "ppt on" in query:
            # Quick presentation creation
            topic = query.replace("create presentation on", "").replace("make presentation on", "")
            topic = topic.replace("create ppt on", "").replace("make ppt on", "").strip()
            
            if topic:
                create_ppt_from_topic(topic, num_slides=7, design_theme="professional")
            else:
                speak("Please specify the topic")
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
            if "send message" in query:
                speak("What message to send")
                message_text = takecommand()  # Changed variable name
                whatsApp(contact_no, message_text, 'message', name)  # Fixed parameters
            elif "phone call" in query:
                whatsApp(contact_no, '', 'call', name)  # Fixed parameters
            else:  # video call
                whatsApp(contact_no, '', 'video call', name)  # Fixed parameters
           else:
            speak("I didn't understand. Please say whatsapp or mobile")
      

        else:
          if query.strip():
             from engine.features import geminiai
             geminiai(query)
    except Exception as e:
        print(f"Error: {e}")
        speak("Sorry, I encountered an error")
    
    eel.ShowHood()


def hotword_listener():
    """Listen for wake word 'IRA'"""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening for 'IRA'...")
        r.adjust_for_ambient_noise(source, duration=0.5)
        
        try:
            audio = r.listen(source, timeout=None, phrase_time_limit=3)
            query = r.recognize_google(audio, language='en-in').lower()
            print(f"Heard: {query}")
            
            if "ira" in query:
                print("✓ Wake word detected!")
                speak("Yes, how can I help?")
                allCommands()
                
        except sr.UnknownValueError:
            # Couldn't understand audio - this is normal, just continue
            pass
        except sr.RequestError as e:
            print(f"Speech recognition service error: {e}")
            time.sleep(2)
        except Exception as e:
            print(f"Hotword error: {e}")
            time.sleep(1)

def start_hotword_thread():
    """Run hotword detection in background"""
    while True:
        try:
            hotword_listener()
        except Exception as e:
            print(f"Hotword thread error: {e}")
            time.sleep(1)


def initialize():
    """Initialize the assistant"""
    print("Initializing Multi-Language Voice Assistant...")
    speak("Voice assistant initialized and ready")
    print(f"Current language: {CURRENT_LANGUAGE}")
    print("Say 'IRA' to activate voice commands")
    
    # Start reminder checker thread
    reminder_thread = threading.Thread(target=reminder_checker, daemon=True)
    reminder_thread.start()
    
    # Start hotword listener thread
    hotword_thread = threading.Thread(target=start_hotword_thread, daemon=True)
    hotword_thread.start()


if __name__ == "__main__":
    initialize()
    
    # Start Eel web interface
    eel.init("web")  # Change "web" to your actual web folder name
    eel.start("index.html", mode='chrome', size=(1000, 600), port=8080)