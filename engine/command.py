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
import subprocess
import pyperclip
import feedparser

import requests
import datetime
from pathlib import Path
import json


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


def find_file_by_name(filename, language="english"):
    """
    Search for a file by name in common locations
    Returns full path if found, None otherwise
    """
    try:
        # Common search locations
        search_paths = [
            Path.home() / "Documents",
            Path.home() / "Downloads",
            Path.home() / "Desktop",
            Path.home() / "Documents" / "IRA_Code_Files",
            Path.home() / "Documents" / "IRA_Presentations",
            Path.home() / "Documents" / "AssistantNotes",
            Path.home() / "Pictures",
            Path.home() / "Music",
            Path.home() / "Videos",
            Path.home(),  # Home directory
        ]
        
        # Clean filename
        filename = filename.strip().lower()
        
        # Replace spoken words with actual symbols
        filename = filename.replace(" dot ", ".")
        filename = filename.replace(" underscore ", "_")
        filename = filename.replace(" dash ", "-")
        
        found_files = []
        
        if language == "hindi":
            speak(f"{filename} को खोजा जा रहा है", language="hindi")
        else:
            speak(f"Searching for {filename}")
        
        print(f"\nSearching for: {filename}")
        print("Searching in common locations...")
        
        for search_path in search_paths:
            if search_path.exists():
                try:
                    # Search in directory and subdirectories
                    for root, dirs, files in os.walk(search_path):
                        for file in files:
                            if filename in file.lower():
                                full_path = os.path.join(root, file)
                                found_files.append(full_path)
                                print(f"Found: {full_path}")
                        
                        # Don't go too deep (max 2 levels)
                        if root.count(os.sep) - str(search_path).count(os.sep) >= 2:
                            dirs.clear()
                            
                except PermissionError:
                    continue
        
        if found_files:
            if len(found_files) == 1:
                if language == "hindi":
                    speak("फ़ाइल मिल गई", language="hindi")
                else:
                    speak("File found")
                return found_files[0]
            else:
                # Multiple files found
                if language == "hindi":
                    speak(f"{len(found_files)} फ़ाइलें मिलीं। पहली फ़ाइल उपयोग की जाएगी", language="hindi")
                else:
                    speak(f"Found {len(found_files)} files. Using the first one")
                
                # Show all found files
                for i, file_path in enumerate(found_files[:5], 1):
                    print(f"{i}. {file_path}")
                
                return found_files[0]
        else:
            if language == "hindi":
                speak(f"{filename} नहीं मिली। कृपया पूरा path बताएं", language="hindi")
            else:
                speak(f"Could not find {filename}. Please provide the full path")
            return None
            
    except Exception as e:
        print(f"File search error: {e}")
        return None


def read_text_file_smart(filename, language="english"):
    """Read text file by searching with filename only"""
    try:
        # Try to find the file
        file_path = find_file_by_name(filename, language)
        
        if not file_path:
            return False
        
        print(f"\nReading file: {file_path}")
        
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read().strip()
        
        if content:
            if language == "hindi":
                speak("फ़ाइल पढ़ी जा रही है", language="hindi")
            else:
                speak("Reading file")
            
            chunks = [content[i:i+2000] for i in range(0, len(content), 2000)]
            
            for chunk in chunks:
                if language == "hindi":
                    speak(chunk, language="hindi")
                else:
                    speak(chunk)
                time.sleep(0.5)
            
            if language == "hindi":
                speak("फ़ाइल पढ़ना पूरा हुआ", language="hindi")
            else:
                speak("Finished reading")
            return True
        else:
            if language == "hindi":
                speak("फ़ाइल खाली है", language="hindi")
            else:
                speak("File is empty")
            return False
            
    except Exception as e:
        print(f"Read error: {e}")
        if language == "hindi":
            speak("फ़ाइल नहीं पढ़ी जा सकी", language="hindi")
        else:
            speak("Could not read the file")
        return False


def read_pdf_file_smart(filename, start_page=0, end_page=None, language="english"):
    """Read PDF file by searching with filename only"""
    try:
        import PyPDF2
        
        file_path = find_file_by_name(filename, language)
        
        if not file_path:
            return False
        
        print(f"\nReading PDF: {file_path}")
        
        with open(file_path, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            num_pages = len(reader.pages)
            
            if end_page is None or end_page > num_pages:
                end_page = num_pages
            
            if start_page < 0 or start_page >= num_pages:
                if language == "hindi":
                    speak("गलत पेज नंबर", language="hindi")
                else:
                    speak("Invalid page number")
                return False
            
            if language == "hindi":
                speak(f"पीडीएफ पढ़ी जा रही है। कुल {num_pages} पेज हैं", language="hindi")
            else:
                speak(f"Reading PDF. Total {num_pages} pages")
            
            for i in range(start_page, end_page):
                try:
                    text = reader.pages[i].extract_text()
                    
                    if text and text.strip():
                        if language == "hindi":
                            speak(f"पेज {i+1}", language="hindi")
                        else:
                            speak(f"Page {i+1}")
                        
                        chunks = [text[j:j+2000] for j in range(0, len(text), 2000)]
                        
                        for chunk in chunks:
                            if language == "hindi":
                                speak(chunk, language="hindi")
                            else:
                                speak(chunk)
                            time.sleep(0.3)
                    else:
                        if language == "hindi":
                            speak(f"पेज {i+1} खाली है", language="hindi")
                        else:
                            speak(f"Page {i+1} is empty")
                            
                except Exception as e:
                    print(f"Error on page {i+1}: {e}")
                    continue
            
            if language == "hindi":
                speak("पीडीएफ पढ़ना पूरा हुआ", language="hindi")
            else:
                speak("Finished reading PDF")
            return True
            
    except ImportError:
        speak("PyPDF2 is not installed. Please run: pip install PyPDF2")
        return False
    except Exception as e:
        print(f"PDF read error: {e}")
        if language == "hindi":
            speak("पीडीएफ नहीं पढ़ी जा सकी", language="hindi")
        else:
            speak("Could not read PDF")
        return False


def read_word_document_smart(filename, language="english"):
    """Read Word document by searching with filename only"""
    try:
        import docx
        
        file_path = find_file_by_name(filename, language)
        
        if not file_path:
            return False
        
        print(f"\nReading Word document: {file_path}")
        
        doc = docx.Document(file_path)
        
        if language == "hindi":
            speak("वर्ड डॉक्यूमेंट पढ़ा जा रहा है", language="hindi")
        else:
            speak("Reading Word document")
        
        full_text = []
        for para in doc.paragraphs:
            if para.text.strip():
                full_text.append(para.text)
        
        content = "\n".join(full_text)
        
        if content:
            chunks = [content[i:i+2000] for i in range(0, len(content), 2000)]
            
            for chunk in chunks:
                if language == "hindi":
                    speak(chunk, language="hindi")
                else:
                    speak(chunk)
                time.sleep(0.3)
            
            if language == "hindi":
                speak("डॉक्यूमेंट पढ़ना पूरा हुआ", language="hindi")
            else:
                speak("Finished reading document")
            return True
        else:
            if language == "hindi":
                speak("डॉक्यूमेंट खाली है", language="hindi")
            else:
                speak("Document is empty")
            return False
            
    except ImportError:
        speak("python-docx is not installed. Please run: pip install python-docx")
        return False
    except Exception as e:
        print(f"Word read error: {e}")
        if language == "hindi":
            speak("वर्ड फ़ाइल नहीं पढ़ी जा सकी", language="hindi")
        else:
            speak("Could not read Word document")
        return False


# Configure Gemini API
GEMINI_API_KEY = "AIzaSyCYDb08-0XuFyK4s5EGzmmtsyieG_PjW1g"
genai.configure(api_key=GEMINI_API_KEY)

def write_code_in_vscode(code_description=None):
    """
    Open VS Code and write code based on voice description
    """
    try:
        if not code_description:
            speak("What code would you like me to write?")
            code_description = takecommand()
            
            if not code_description or len(code_description.strip()) < 3:
                speak("Code description not recognized")
                return False
        
        speak(f"Generating code for: {code_description}")
        print(f"\nAttempting to generate code for: {code_description}")
        print("Sending request to Gemini API...")
        
        # Try different model names in order (updated for 2025)
        model_names = [
            'gemini-2.0-flash-exp',      # Latest experimental model
            'gemini-1.5-flash-002',       # Stable flash model
            'gemini-1.5-pro-002',         # Stable pro model
            'gemini-1.0-pro',             # Fallback legacy model
        ]
        
        generated_code = None
        successful_model = None
        last_error = None
        
        for model_name in model_names:
            try:
                print(f"Trying model: {model_name}")
                model = genai.GenerativeModel(model_name)
                
                prompt = f"""Write clean, well-commented code for: {code_description}

Requirements:
- Include helpful comments explaining the logic
- Follow best practices and conventions
- Add basic error handling where appropriate
- Make the code production-ready and functional

Return ONLY the code without any explanations or markdown formatting."""
                
                response = model.generate_content(prompt)
                
                if response and response.text:
                    generated_code = response.text.strip()
                    successful_model = model_name
                    print(f"✓ Successfully generated code using {model_name}")
                    break
                    
            except Exception as e:
                error_msg = str(e)
                last_error = error_msg
                print(f"✗ Failed with {model_name}: {error_msg[:150]}")
                
                # Extract error type for better debugging
                if "404" in error_msg:
                    print(f"  Error type: NotFound")
                elif "429" in error_msg:
                    print(f"  Error type: RateLimitExceeded")
                elif "403" in error_msg:
                    print(f"  Error type: PermissionDenied")
                
                continue
        
        if not generated_code:
            print(f"AI generation failed: All AI models failed")
            speak("AI generation failed. Creating a template file instead")
            
            # Create template based on description
            desc_lower = code_description.lower()
            
            if 'python' in desc_lower or 'calculator' in desc_lower or 'script' in desc_lower:
                generated_code = f'''# {code_description}
# Generated by IRA - Template
# Created: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

def main():
    """
    TODO: Implement {code_description}
    """
    print("Hello from {code_description}")
    # Add your implementation here
    pass

if __name__ == "__main__":
    main()
'''
            elif 'html' in desc_lower or 'webpage' in desc_lower or 'website' in desc_lower:
                generated_code = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{code_description}</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 20px;
            padding: 20px;
        }}
    </style>
</head>
<body>
    <h1>{code_description}</h1>
    <p>TODO: Add your content here</p>
    
    <script>
        // Add your JavaScript here
        console.log('Page loaded');
    </script>
</body>
</html>'''
            else:
                generated_code = f'''// {code_description}
// Generated by IRA - Template
// Created: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

function main() {{
    // TODO: Implement {code_description}
    console.log("Hello from {code_description}");
}}

main();
'''
        else:
            # Clean markdown formatting from AI response
            generated_code = generated_code.replace('```python', '').replace('```javascript', '')
            generated_code = generated_code.replace('```java', '').replace('```html', '')
            generated_code = generated_code.replace('```css', '').replace('```', '').strip()
        
        # Determine file extension
        ext = 'py'
        desc_lower = code_description.lower()
        
        if 'javascript' in desc_lower or 'js' in desc_lower or 'node' in desc_lower:
            ext = 'js'
        elif 'java' in desc_lower and 'javascript' not in desc_lower:
            ext = 'java'
        elif 'html' in desc_lower or 'webpage' in desc_lower or 'website' in desc_lower:
            ext = 'html'
        elif 'css' in desc_lower or 'style' in desc_lower:
            ext = 'css'
        elif 'c++' in desc_lower or 'cpp' in desc_lower:
            ext = 'cpp'
        elif 'c#' in desc_lower or 'csharp' in desc_lower:
            ext = 'cs'
        
        # Create code directory
        code_dir = Path.home() / "Documents" / "IRA_Code_Files"
        code_dir.mkdir(parents=True, exist_ok=True)
        
        # Generate filename
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_name = "".join(c if c.isalnum() or c in ('_', '-') else '_' 
                          for c in code_description[:40]).strip('_')
        filename = code_dir / f"{safe_name}_{timestamp}.{ext}"
        
        # Write file
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(generated_code)
        
        print(f"✓ File saved: {filename}")
        speak("Code file created successfully")
        
        # Open VS Code
        time.sleep(0.5)
        
        try:
            system_os = platform.system()
            
            if system_os == "Windows":
                # Try multiple methods to open VS Code
                try:
                    # Method 1: Direct code command
                    result = subprocess.run(
                        ["code", str(filename)], 
                        capture_output=True,
                        text=True,
                        timeout=10
                    )
                    
                    if result.returncode == 0:
                        speak("Opening in Visual Studio Code")
                        time.sleep(2)
                        return True
                    else:
                        raise Exception("code command returned non-zero")
                        
                except (FileNotFoundError, Exception) as e:
                    print(f"VS Code command failed: {e}")
                    
                    # Method 2: Try common VS Code installation paths
                    vscode_paths = [
                        r"C:\Users\{}\AppData\Local\Programs\Microsoft VS Code\Code.exe".format(os.getenv('USERNAME')),
                        r"C:\Program Files\Microsoft VS Code\Code.exe",
                        r"C:\Program Files (x86)\Microsoft VS Code\Code.exe",
                    ]
                    
                    for vscode_path in vscode_paths:
                        if os.path.exists(vscode_path):
                            subprocess.Popen([vscode_path, str(filename)])
                            speak("Opening in Visual Studio Code")
                            time.sleep(2)
                            return True
                    
                    # Method 3: Fallback to notepad
                    print("VS Code not found. Opening in Notepad...")
                    speak("Visual Studio Code not found. Opening in Notepad instead")
                    subprocess.Popen(["notepad.exe", str(filename)])
                    time.sleep(1)
                    return True
                    
            elif system_os == "Darwin":  # macOS
                subprocess.run(["open", "-a", "Visual Studio Code", str(filename)], timeout=5)
                speak("Opening in Visual Studio Code")
                
            elif system_os == "Linux":
                subprocess.run(["code", str(filename)], timeout=5)
                speak("Opening in Visual Studio Code")
            
            time.sleep(2)
            return True
            
        except Exception as open_error:
            print(f"Error opening file: {open_error}")
            speak("File created successfully. Please open it manually from your Documents folder")
            
            # Try to open folder instead
            try:
                if system_os == "Windows":
                    os.startfile(str(code_dir))
                elif system_os == "Darwin":
                    subprocess.run(["open", str(code_dir)])
                elif system_os == "Linux":
                    subprocess.run(["xdg-open", str(code_dir)])
            except:
                pass
            
            return True
        
    except Exception as e:
        print(f"Function error: {e}")
        import traceback
        traceback.print_exc()
        speak("Sorry, I encountered an error while generating the code")
        return False


def open_file_in_vscode(file_path):
    """
    Open a specific file in VS Code
    """
    try:
        # Normalize the path
        file_path = file_path.strip()
        file_path = file_path.replace(" slash ", "/").replace(" backslash ", "\\")
        file_path = file_path.replace("see colon", "C:").replace("c colon", "C:")
        file_path = file_path.replace("d colon", "D:").replace("dee colon", "D:")
        
        # Expand user path and make absolute
        file_path = os.path.expanduser(file_path)
        file_path = os.path.abspath(file_path)
        
        # Check if file exists
        if not os.path.exists(file_path):
            speak("The specified file does not exist. Please check the path.")
            print(f"File not found: {file_path}")
            return False
        
        speak("Opening file in Visual Studio Code")
        
        system_os = platform.system()
        
        if system_os == "Windows":
            try:
                # Try code command first
                subprocess.Popen(["code", file_path])
                time.sleep(2)
                speak("File opened successfully")
                return True
            except FileNotFoundError:
                # Fallback to default application
                speak("VS Code not found. Opening with default application")
                os.startfile(file_path)
                time.sleep(1)
                return True
                
        elif system_os == "Darwin":
            subprocess.Popen(["open", "-a", "Visual Studio Code", file_path])
            
        elif system_os == "Linux":
            subprocess.Popen(["code", file_path])
        
        time.sleep(2)
        speak("File opened successfully")
        return True
        
    except Exception as e:
        print(f"Open file error: {e}")
        speak("Sorry, I could not open the file")
        return False


def save_current_code_from_vscode(filename=None):
    """
    Save the current VS Code file with a specific name using keyboard automation
    """
    try:
        import pyautogui
        
        if not filename:
            speak("What should be the filename?")
            filename = takecommand()
        
        if filename:
            # Ctrl+Shift+S (Save As)
            pyautogui.hotkey('ctrl', 'shift', 's')
            time.sleep(1.5)
            
            # Clear any existing text
            pyautogui.hotkey('ctrl', 'a')
            time.sleep(0.3)
            
            # Type filename
            pyautogui.write(filename, interval=0.05)
            time.sleep(0.5)
            
            # Press Enter to save
            pyautogui.press('enter')
            time.sleep(0.5)
            
            speak(f"File saved as {filename}")
            return True
        else:
            speak("Filename not recognized")
            return False
            
    except Exception as e:
        print(f"Save file error: {e}")
        speak("Sorry, I could not save the file")
        return False




# News API Configuration (Optional)
NEWS_API_KEY = "20af6c9482b74c778676063604441009"  # Get from https://newsapi.org/register
NEWS_API_BASE_URL = "https://newsapi.org/v2/"
def get_news_hindi_from_rss(language="hindi"):
    """
    Fetch news using RSS feeds - Supports Hindi and English
    """
    try:
        import feedparser
        
        if language == "hindi":
            speak("हिंदी समाचार लाया जा रहा है")
            print("Fetching Hindi news from RSS feeds...")
            
            # Updated Hindi news RSS feeds with working URLs
            rss_feeds = {
                "आज तक": "https://www.aajtak.in/rss/top-stories",
                "BBC हिंदी": "https://feeds.bbci.co.uk/hindi/rss.xml",
                "न्यूज़18": "https://hindi.news18.com/rss/india.xml",
                "वन इंडिया": "https://hindi.oneindia.com/rss/news-fb.xml",
            }
        else:
            speak("Fetching latest news headlines")
            print("Fetching English news from RSS feeds...")
            
            # English news RSS feeds
            rss_feeds = {
                "BBC": "http://feeds.bbci.co.uk/news/rss.xml",
                "The Hindu": "https://www.thehindu.com/news/national/feeder/default.rss",
                "India Today": "https://www.indiatoday.in/rss/home",
                "NDTV": "https://feeds.feedburner.com/ndtvnews-top-stories",
            }
        
        all_articles = []
        
        for source_name, feed_url in rss_feeds.items():
            try:
                print(f"Fetching from {source_name}...")
                # Add timeout and user agent to avoid blocks
                feed = feedparser.parse(feed_url, 
                                       request_headers={'User-Agent': 'Mozilla/5.0'})
                
                # Check if feed was fetched successfully
                if feed.entries:
                    for entry in feed.entries[:3]:  # Get top 3 from each source
                        all_articles.append({
                            "source": source_name,
                            "title": entry.get("title", "No title"),
                            "summary": entry.get("summary", "")[:150]
                        })
                    print(f"✓ Got {len(feed.entries[:3])} articles from {source_name}")
                else:
                    print(f"⚠ No articles from {source_name}")
                    
            except Exception as e:
                print(f"✗ Error fetching from {source_name}: {e}")
                continue
        
        if all_articles:
            if language == "hindi":
                speak(f"यहां {len(all_articles)} मुख्य समाचार हैं:")
            else:
                speak(f"Here are the latest {len(all_articles)} headlines:")
            
            for i, article in enumerate(all_articles, 1):
                headline = f"{article['title']}"
                print(f"{i}. [{article['source']}] {headline}")
                
                # Speak in appropriate language
                if language == "hindi":
                    speak(f"समाचार {i}, {article['source']} से: {headline}", language="hindi")
                else:
                    speak(f"Headline {i} from {article['source']}: {headline}")
                time.sleep(1)
            
            return True
        else:
            if language == "hindi":
                speak("समाचार प्राप्त नहीं हो सका। कृपया अपना इंटरनेट कनेक्शन जांचें")
            else:
                speak("Could not fetch news. Please check your internet connection")
            return False
            
    except ImportError:
        print("\n⚠️ feedparser not installed")
        if language == "hindi":
            speak("कृपया feedparser लाइब्रेरी इंस्टॉल करें। कमांड प्रॉम्प्ट में टाइप करें: pip install feedparser")
        else:
            speak("Please install feedparser library. Type in command prompt: pip install feedparser")
        return False
    except Exception as e:
        print(f"RSS feed error: {e}")
        import traceback
        traceback.print_exc()
        if language == "hindi":
            speak("समाचार प्राप्त करने में त्रुटि हुई। इंटरनेट कनेक्शन जांचें")
        else:
            speak("Error fetching news. Please check your internet connection")
        return False
def get_news_from_rss():
    """
    Fetch news using RSS feeds - NO API KEY REQUIRED
    This will always work without any configuration
    """
    try:
        import feedparser
        
        speak("Fetching latest news headlines")
        print("Fetching news from RSS feeds...")
        
        # Popular Indian news RSS feeds
        rss_feeds = {
            "NDTV": "https://feeds.feedburner.com/ndtvnews-top-stories",
            "The Hindu": "https://www.thehindu.com/news/national/feeder/default.rss",
            "India Today": "https://www.indiatoday.in/rss/home",
        }
        
        all_articles = []
        
        for source_name, feed_url in rss_feeds.items():
            try:
                print(f"Fetching from {source_name}...")
                feed = feedparser.parse(feed_url)
                
                for entry in feed.entries[:3]:  # Get top 3 from each source
                    all_articles.append({
                        "source": source_name,
                        "title": entry.get("title", "No title"),
                        "summary": entry.get("summary", "")[:150]  # First 150 chars
                    })
            except Exception as e:
                print(f"Error fetching from {source_name}: {e}")
                continue
        
        if all_articles:
            speak(f"Here are the latest {len(all_articles)} headlines:")
            
            for i, article in enumerate(all_articles, 1):
                headline = f"{article['title']}"
                print(f"{i}. [{article['source']}] {headline}")
                speak(f"Headline {i} from {article['source']}: {headline}")
                time.sleep(1)
            
            return True
        else:
            speak("Could not fetch news from RSS feeds. Please check your internet connection")
            return False
            
    except ImportError:
        print("\n⚠️ feedparser not installed")
        speak("Please install feedparser library. Open command prompt and type: pip install feedparser")
        return False
    except Exception as e:
        print(f"RSS feed error: {e}")
        speak("Could not fetch news. Please check your internet connection")
        return False


def get_news_from_api(category="general", country="in", max_articles=5):
    """
    Fetch news using NewsAPI.org - REQUIRES API KEY
    Categories: business, entertainment, general, health, science, sports, technology
    """
    try:
        # Check if API key is configured
        if not NEWS_API_KEY or NEWS_API_KEY == "YOUR_NEWS_API_KEY_HERE":
            print("⚠️ NewsAPI key not configured, falling back to RSS feeds")
            return get_news_from_rss()
        
        speak(f"Fetching latest {category} news")
        print(f"Fetching {category} news from NewsAPI...")
        
        url = f"{NEWS_API_BASE_URL}top-headlines"
        params = {
            "country": country,
            "category": category,
            "apiKey": NEWS_API_KEY,
            "pageSize": max_articles
        }
        
        response = requests.get(url, params=params, timeout=15)
        
        if response.status_code == 200:
            data = response.json()
            articles = data.get("articles", [])
            
            if articles:
                speak(f"Here are the top {len(articles)} {category} headlines:")
                
                for i, article in enumerate(articles, 1):
                    title = article.get("title", "No title")
                    source = article.get("source", {}).get("name", "Unknown")
                    
                    print(f"{i}. [{source}] {title}")
                    speak(f"Headline {i}: {title}")
                    time.sleep(1)
                
                return True
            else:
                print(f"No articles found for category: {category}")
                speak(f"No {category} news found. Let me try general news instead")
                return get_news_from_rss()
        
        elif response.status_code == 401:
            print("❌ Invalid API key")
            speak("News API key is invalid. Switching to RSS feeds")
            return get_news_from_rss()
        
        elif response.status_code == 426:
            print("❌ API key requires upgrade")
            speak("News API requires upgrade. Using free RSS feeds instead")
            return get_news_from_rss()
        
        elif response.status_code == 429:
            print("❌ API rate limit exceeded")
            speak("News API limit reached. Using RSS feeds instead")
            return get_news_from_rss()
        
        else:
            print(f"API returned status code: {response.status_code}")
            speak("News API unavailable. Using RSS feeds instead")
            return get_news_from_rss()
            
    except requests.Timeout:
        print("⚠️ Request timed out")
        speak("Request timed out. Trying RSS feeds")
        return get_news_from_rss()
    except Exception as e:
        print(f"NewsAPI error: {e}")
        speak("News API error. Using RSS feeds instead")
        return get_news_from_rss()


def get_news_gnews_free():
    """
    Alternative free news source using web scraping techniques
    No API key needed
    """
    try:
        speak("Fetching latest news")
        
        # Using a public news aggregator
        url = "https://newsapi.org/v2/top-headlines?country=in&apiKey=demo"
        
        # Note: The demo key has very limited access
        response = requests.get(url, timeout=10)
        
        if response.status_code != 200:
            return get_news_from_rss()
        
        return True
        
    except Exception as e:
        print(f"Free news fetch error: {e}")
        return get_news_from_rss()


def search_news(query, max_articles=5):
    """
    Search for specific news topics
    """
    try:
        if not NEWS_API_KEY or NEWS_API_KEY == "YOUR_NEWS_API_KEY_HERE":
            speak(f"Searching for {query} in RSS feeds")
            return search_news_rss(query)
        
        speak(f"Searching news about {query}")
        
        url = f"{NEWS_API_BASE_URL}everything"
        params = {
            "q": query,
            "language": "en",
            "sortBy": "publishedAt",
            "apiKey": NEWS_API_KEY,
            "pageSize": max_articles
        }
        
        response = requests.get(url, params=params, timeout=15)
        
        if response.status_code == 200:
            data = response.json()
            articles = data.get("articles", [])
            
            if articles:
                speak(f"Found {len(articles)} articles about {query}:")
                
                for i, article in enumerate(articles, 1):
                    title = article.get("title", "No title")
                    source = article.get("source", {}).get("name", "Unknown")
                    
                    print(f"{i}. [{source}] {title}")
                    speak(f"Article {i}: {title}")
                    time.sleep(1)
                
                return True
            else:
                speak(f"No articles found about {query}")
                return False
        else:
            return search_news_rss(query)
            
    except Exception as e:
        print(f"News search error: {e}")
        return search_news_rss(query)


def search_news_rss(query):
    """
    Search news in RSS feeds (basic filtering)
    """
    try:
        import feedparser
        
        speak(f"Searching for {query} in news feeds")
        
        feeds = [
            "https://feeds.feedburner.com/ndtvnews-top-stories",
            "https://www.thehindu.com/news/national/feeder/default.rss",
        ]
        
        matching_articles = []
        query_lower = query.lower()
        
        for feed_url in feeds:
            try:
                feed = feedparser.parse(feed_url)
                for entry in feed.entries:
                    title = entry.get("title", "").lower()
                    if query_lower in title:
                        matching_articles.append(entry.get("title", ""))
            except:
                continue
        
        if matching_articles:
            speak(f"Found {len(matching_articles)} articles about {query}")
            for i, title in enumerate(matching_articles[:5], 1):
                speak(f"Article {i}: {title}")
                time.sleep(1)
            return True
        else:
            speak(f"No articles found about {query}")
            return False
            
    except ImportError:
        speak("Cannot search news. Please install feedparser")
        return False
    except Exception as e:
        print(f"RSS search error: {e}")
        return False


def get_current_affairs():
    """
    Main function - automatically chooses best method
    ALWAYS WORKS - uses RSS feeds as reliable fallback
    """
    try:
        # Try API first if configured
        if NEWS_API_KEY and NEWS_API_KEY != "YOUR_NEWS_API_KEY_HERE":
            print("Trying NewsAPI...")
            return get_news_from_api(category="general", country="in")
        else:
            # Use RSS feeds (always works)
            print("Using RSS feeds (no API key configured)...")
            return get_news_from_rss()
            
    except Exception as e:
        print(f"Current affairs error: {e}")
        # Last resort - always try RSS
        return get_news_from_rss()


def get_business_news():
    """Get business news"""
    return get_news_from_api(category="business", country="in")


def get_sports_news():
    """Get sports news"""
    return get_news_from_api(category="sports", country="in")


def get_tech_news():
    """Get technology news"""
    return get_news_from_api(category="technology", country="in")


def get_entertainment_news():
    """Get entertainment news"""
    return get_news_from_api(category="entertainment", country="in")


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

        elif "what is unique" in query or "what makes you different" in query or "what makes you special" in query or "your uniqueness" in query or "why choose you" in query or "your specialty" in query:
         
           # Speak in smaller chunks for better clarity
            speak("Let me tell you what makes me truly special and different from other assistants.")
            time.sleep(0.2)
    
            speak("First, I am truly multilingual. I speak over 27 languages including English, Hindi, Spanish, French, German, Tamil, Telugu, Bengali, Arabic, Chinese, Japanese, Korean, and many more. You can switch between any language anytime.")
            time.sleep(0.2)
    
            speak("I offer comprehensive system control. I manage Wi-Fi, reveal passwords, monitor disk usage, check CPU and RAM, control brightness and volume, capture screenshots, and safely control your PC operations.")
            time.sleep(0.2)
    
            speak("My file management is exceptional. I read text, PDF, and Word documents in English and Hindi. Just say the file name - I'll find it automatically in your common folders.")
            time.sleep(0.2)
    
            speak("I have artificial intelligence for creative tasks. I generate images from descriptions, create professional PowerPoint presentations with custom themes, and write complete code in multiple programming languages.")
            time.sleep(0.2)
    
            speak("I keep you updated with latest news in English and Hindi from reliable sources. I search specific topics and provide business, sports, technology, and entertainment updates.")
            time.sleep(0.2)
    
            speak("I offer practical utilities like weather forecasts, Wikipedia searches, internet speed tests, battery monitoring, and system diagnostics. I also manage tasks, set reminders, and take notes.")
            time.sleep(0.2)
    
            speak("What truly sets me apart is my voice-first design in your preferred language. Just say IRA and I start listening. I translate between languages and adapt to you automatically.")
            time.sleep(0.2)
    
            speak("I was created by Ankita, Anjali, Shubham, and Amrita to make technology accessible to everyone. I'm your personal productivity partner, system administrator, creative collaborator, and information companion, all in one, speaking your language.")
        elif "read file" in query or "read text" in query or "फ़ाइल पढ़ो" in query:
            speak("What is the file name?")
            filename = takecommand()
    
            if filename:
               speak("Should I read in English or Hindi?")
               lang_choice = takecommand()
        
               lang = "hindi" if "hindi" in lang_choice or "हिंदी" in lang_choice else "english"
               read_text_file_smart(filename, language=lang)
            else:
               speak("File name not recognized")

        elif "read pdf" in query or "पीडीएफ पढ़ो" in query:
            speak("What is the PDF file name?")
            filename = takecommand()
    
            if filename:
              speak("Should I read in English or Hindi?")
              lang_choice = takecommand()
        
              lang = "hindi" if "hindi" in lang_choice or "हिंदी" in lang_choice else "english"
        
              speak("Should I read all pages or specific pages?")
              page_choice = takecommand()
        
              if "specific" in page_choice:
                speak("From which page?")
                start_text = takecommand()
                try:
                  start_page = int(''.join(filter(str.isdigit, start_text))) - 1
                except:
                  start_page = 0
            
                speak("To which page?")
                end_text = takecommand()
                try:
                  end_page = int(''.join(filter(str.isdigit, end_text)))
                except:
                  end_page = None
            
                read_pdf_file_smart(filename, start_page, end_page, language=lang)
              else:
                 read_pdf_file_smart(filename, language=lang)
            else:
              speak("File name not recognized")

        elif "read word" in query or "read document" in query or "वर्ड पढ़ो" in query:
             speak("What is the Word document name?")
             filename = takecommand()
    
             if filename:
               speak("Should I read in English or Hindi?")
               lang_choice = takecommand()
        
               lang = "hindi" if "hindi" in lang_choice or "हिंदी" in lang_choice else "english"
               read_word_document_smart(filename, language=lang)
             else:
               speak("File name not recognized")
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
        # Add these elif conditions in the allCommands() function:

        elif "write code" in query and ("vs code" in query or "visual studio" in query):
            speak("What code would you like me to write?")
            code_description = takecommand()
            
            if code_description:
                write_code_in_vscode(code_description)
            else:
                speak("Code description not recognized")
        
        elif "open vs code" in query or "launch vs code" in query or "start vs code" in query:
            write_code_in_vscode()
        
        elif "save code" in query or "save file" in query:
            save_current_code_from_vscode()
        elif "hindi news" in query or "हिंदी समाचार" in query or "hindi mein news" in query:
          get_news_hindi_from_rss(language="hindi")
    
        elif "news in hindi" in query or "समाचार सुनाओ" in query:
           get_news_hindi_from_rss(language="hindi")
        elif "news" in query or "current affairs" in query or "headlines" in query:
           if "business" in query:
             get_business_news()
           elif "sports" in query:
             get_sports_news()
           elif "technology" in query or "tech" in query:
             get_tech_news()
           elif "entertainment" in query:
             get_entertainment_news()
           else:
             get_current_affairs()

        elif "search news" in query or "news about" in query:
           topic = query.replace("search news", "").replace("news about", "")
           topic = topic.replace("for", "").strip()
    
           if topic:
            search_news(topic)
           else:
            speak("What topic should I search for?")
            topic = takecommand()
            if topic:
              search_news(topic)  
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