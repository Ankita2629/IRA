import datetime
import os
import re
from shlex import quote
import sqlite3
import struct
import subprocess
import time
import webbrowser
import PyPDF2
from playsound import playsound
import eel
import psutil
import pvporcupine
import pyaudio
import pyautogui
import requests
from engine.command import speak
from engine.config import ASSISTANT_NAME, LLM_KEY
import pywhatkit as kit
from engine.helper import extract_yt_term, markdown_to_text, remove_words
import datetime

# Database connection
con = sqlite3.connect("ira.db")
cursor = con.cursor()

@eel.expose
def playAssistantSound():
    """Play assistant start sound"""
    music_dir = "www\\assests\\audio\\start_sound.mp3"
    playsound(music_dir)


def openCommand(query):
    """Open applications or websites based on voice command"""
    query = query.replace(ASSISTANT_NAME, "")
    query = query.replace("open", "")
    query = query.lower()

    app_name = query.strip()

    if app_name != "":
        try:
            # First, try to find in system commands
            cursor.execute(
                'SELECT path FROM sys_command WHERE name IN (?)', (app_name,))
            results = cursor.fetchall()

            if len(results) != 0:
                speak("Opening " + query)
                os.startfile(results[0][0])

            elif len(results) == 0: 
                # If not found, try web commands
                cursor.execute(
                'SELECT url FROM web_command WHERE name IN (?)', (app_name,))
                results = cursor.fetchall()
                
                if len(results) != 0:
                    speak("Opening " + query)
                    webbrowser.open(results[0][0])
                else:
                    # Try to open using system command
                    speak("Opening " + query)
                    try:
                        os.system('start ' + query)
                    except:
                        speak("Application not found")
        except Exception as e:
            print(f"Open command error: {e}")
            speak("Something went wrong")


def PlayYoutube(query):
    """Play video on YouTube"""
    try:
        search_term = extract_yt_term(query)
        speak("Playing " + search_term + " on YouTube")
        kit.playonyt(search_term)
    except Exception as e:
        print(f"YouTube error: {e}")
        speak("Could not play on YouTube")

def hotword():
    """Listen for wake word (IRA/Alexa)"""
    porcupine = None
    paud = None
    audio_stream = None
    
    try:
        # Custom and default keyword
        porcupine = pvporcupine.create(
            access_key="K0DUIHSYae4NMEKAwQv0p94OAvAH8MNvKdebIuZi0lEq+vsUobC5Gg==",  # from console.picovoice.ai
            keyword_paths=[r"C:\Users\ankit\Desktop\IRA\wake-up-ira_en_windows_v3_0_0.ppn"],
            keywords=["wake up ira"]
        )
        # Loop for streaming
        while True:
            keyword = audio_stream.read(porcupine.frame_length)
            keyword = struct.unpack_from("h" * porcupine.frame_length, keyword)

            # Processing keyword from mic 
            keyword_index = porcupine.process(keyword)

            # Check if keyword detected
            if keyword_index >= 0:
                print("Hotword detected")

                # Press shortcut key Win+J
                import pyautogui as autogui
                autogui.keyDown("win")
                autogui.press("i")
                time.sleep(2)
                autogui.keyUp("win")
                
    except Exception as e:
        print(f"Hotword error: {e}")
    finally:
        if porcupine is not None:
            porcupine.delete()
        if audio_stream is not None:
            audio_stream.close()
        if paud is not None:
            paud.terminate()


def findContact(query):
    """Find contact from database"""
    # Fixed typo: 'wahtsapp' -> 'whatsapp'
    words_to_remove = [ASSISTANT_NAME, 'make', 'a', 'to', 'phone', 'call', 'send', 'message', 'whatsapp', 'video']
    query = remove_words(query, words_to_remove)

    try:
        query = query.strip().lower()
        cursor.execute(
            "SELECT mobile_no FROM contacts WHERE LOWER(name) LIKE ? OR LOWER(name) LIKE ?", 
            ('%' + query + '%', query + '%')
        )
        results = cursor.fetchall()
        
        if results:
            print(results[0][0])
            mobile_number_str = str(results[0][0])

            # Add country code if not present
            if not mobile_number_str.startswith('+91'):
                mobile_number_str = '+91' + mobile_number_str

            return mobile_number_str, query
        else:
            speak('Contact does not exist')
            return 0, 0
            
    except Exception as e:
        print(f"Find contact error: {e}")
        speak('Contact not found')
        return 0, 0


def whatsApp(mobile_no, message, flag, name):
    """
    Send WhatsApp message or make call using desktop app
    flag: 'message', 'call', or 'video call'
    """
    try:
        # Ensure phone number format
        if not mobile_no.startswith('+'):
            mobile_no = '+91' + mobile_no
        
        # Set parameters based on action type
        if flag == 'message':
            target_tab = 18
            ira_message = "Message sent successfully to " + name
        elif flag == 'call':
            target_tab = 6
            message = ''
            ira_message = "Calling " + name
        else:  # video call
            target_tab = 11
            message = ''
            ira_message = "Starting video call with " + name

        # Encode the message for URL
        encoded_message = quote(message)
        print(f"Encoded message: {encoded_message}")
        
        # Construct the WhatsApp URL
        whatsapp_url = f"whatsapp://send?phone={mobile_no}&text={encoded_message}"

        # Construct the full command
        full_command = f'start "" "{whatsapp_url}"'

        # Open WhatsApp with the constructed URL
        subprocess.run(full_command, shell=True)
        time.sleep(5)
        subprocess.run(full_command, shell=True)
        
        # Use Ctrl+F to open search
        pyautogui.hotkey('ctrl', 'f')
        time.sleep(1)

        # Navigate using Tab key
        for i in range(1, target_tab):
            pyautogui.hotkey('tab')
            time.sleep(0.1)

        # Press Enter to execute
        time.sleep(0.5)
        pyautogui.hotkey('enter')
        
        speak(ira_message)
        return True
        
    except Exception as e:
        print(f"WhatsApp error: {e}")
        speak(f"Failed to complete WhatsApp action for {name}")
        return False


def whatsApp_web(mobile_no, message, flag, name):
    """
    Alternative WhatsApp method using pywhatkit (WhatsApp Web)
    More reliable but opens browser
    """
    try:
        # Ensure phone number format
        if not mobile_no.startswith('+'):
            mobile_no = '+91' + mobile_no
        
        if flag == 'message':
            # Schedule message 2 minutes from now
            now = datetime.datetime.now()
            hour = now.hour
            minute = now.minute + 2
            
            if minute >= 60:
                hour += 1
                minute -= 60
            
            print(f"Scheduling WhatsApp message to {name} at {hour}:{minute}")
            kit.sendwhatmsg(mobile_no, message, hour, minute, wait_time=20, tab_close=True)
            speak(f"Message will be sent to {name}")
            return True
            
        elif flag == 'call' or flag == 'video call':
            # Open WhatsApp Web with contact
            clean_number = mobile_no.replace('+', '')
            url = f"https://wa.me/{clean_number}"
            webbrowser.open(url)
            speak(f"Opening WhatsApp Web for {name}")
            return True
            
    except Exception as e:
        print(f"WhatsApp Web error: {e}")
        return False


def sendMessage(message, mobile_no, name):
    """Send SMS using default messaging app"""
    try:
        import urllib.parse
        
        # Clean phone number
        mobile_no = mobile_no.replace('+', '').replace('-', '').replace(' ', '')
        
        # Create SMS URL
        encoded_message = urllib.parse.quote(message)
        sms_url = f"sms:{mobile_no}?body={encoded_message}"
        
        webbrowser.open(sms_url)
        speak(f"SMS opened for {name}")
        return True
        
    except Exception as e:
        print(f"SMS error: {e}")
        speak("Could not send SMS")
        return False


def makeCall(name, mobile_no):
    """Make phone call using tel: protocol"""
    try:
        # Clean phone number
        mobile_no = mobile_no.replace('+', '').replace('-', '').replace(' ', '')
        
        # Create call URL
        call_url = f"tel:{mobile_no}"
        webbrowser.open(call_url)
        
        speak(f"Calling {name}")
        return True
        
    except Exception as e:
        print(f"Call error: {e}")
        speak("Could not make call")
        return False


def geminiai(query):
    """Get AI response using Google Gemini"""
    try:
        import google.generativeai as genai
        
        query = query.replace(ASSISTANT_NAME, "")
        query = query.replace("search", "")
        
        # Set your API key
        genai.configure(api_key=LLM_KEY)

        # Select a model 
        model = genai.GenerativeModel("gemini-2.0-flash")

        # Generate a response
        response = model.generate_content(query)
        filter_text = markdown_to_text(response.text)
        speak(filter_text)
        
        return filter_text
        
    except Exception as e:
        print(f"Gemini AI Error: {e}")
        speak("Sorry, I couldn't process that request")
        return None




# Contact management functions
def add_contact(name, phone_number):
    """Add new contact to database"""
    try:
        cursor.execute(
            "INSERT INTO contacts (name, mobile_no) VALUES (?, ?)",
            (name.lower(), phone_number)
        )
        con.commit()
        speak(f"Contact {name} added successfully")
        return True
    except Exception as e:
        print(f"Add contact error: {e}")
        speak("Could not add contact")
        return False


def list_contacts(limit=10):
    """List all contacts from database"""
    try:
        cursor.execute(f"SELECT name, mobile_no FROM contacts LIMIT {limit}")
        contacts = cursor.fetchall()
        
        if contacts:
            speak(f"You have {len(contacts)} contacts")
            for name, phone in contacts:
                speak(f"{name}: {phone}")
        else:
            speak("No contacts found")
        
        return contacts
    except Exception as e:
        print(f"List contacts error: {e}")
        return []


def delete_contact(name):
    """Delete contact from database"""
    try:
        cursor.execute("DELETE FROM contacts WHERE LOWER(name) = ?", (name.lower(),))
        
        if cursor.rowcount > 0:
            con.commit()
            speak(f"Contact {name} deleted successfully")
            return True
        else:
            speak(f"Contact {name} not found")
            return False
    except Exception as e:
        print(f"Delete contact error: {e}")
        speak("Could not delete contact")
        return False


# Testing function
if __name__ == "__main__":
    print("Testing features module...")
    
    # Test contact search
    mobile, name = findContact("send message to john")
    print(f"Found: {name} - {mobile}")
    print(f"Found: {name} - {mobile}")
