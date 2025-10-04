# IRA - Intelligent Responsive Assistant

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.8+-green.svg)
![License](https://img.shields.io/badge/license-MIT-orange.svg)

**IRA** is a powerful, multilingual voice assistant that combines advanced AI capabilities with comprehensive system control. Created by Ankita Singh, IRA is designed to make technology accessible to everyone through natural voice interaction in over 27 languages.

## 🌟 Key Features

### 🌍 Multilingual Support (27+ Languages)
- **Supported Languages**: English, Hindi, Spanish, French, German, Italian, Portuguese, Russian, Japanese, Chinese, Arabic, Korean, Tamil, Telugu, Bengali, Marathi, Gujarati, Kannada, Malayalam, Punjabi, Urdu, Thai, Vietnamese, Indonesian, Dutch, Polish, Turkish
- Switch languages on-the-fly with voice commands
- Real-time translation between any supported languages
- Native text-to-speech in all languages

### 💻 Comprehensive System Control
- **Power Management**: Shutdown, restart, sleep, and lock PC
- **Volume Control**: Increase, decrease, and mute system volume
- **Display Control**: Adjust screen brightness dynamically
- **Screenshots**: Capture and save screenshots automatically
- **Battery Monitoring**: Check battery status and charging state
- **System Diagnostics**: Monitor CPU usage, RAM usage, and disk space

### 📡 Advanced Network Management
- View current Wi-Fi connection information
- Display local and network IP addresses
- Retrieve saved Wi-Fi passwords (Windows)
- Scan and list available Wi-Fi networks
- Check internet connection speed with detailed metrics

### 📄 Intelligent File Management
- **Smart File Search**: Find files by name across common directories
- **Multi-Format Reading**: 
  - Text files (.txt)
  - PDF documents with page selection
  - Word documents (.docx)
- **Bilingual Support**: Read documents in English or Hindi
- **Voice Control**: Create, read, and manage files hands-free
- **Auto-Detection**: Automatically locates files in standard folders

### 🤖 AI-Powered Creative Tools

#### Image Generation
- Generate images from text descriptions
- Multiple AI services: Pollinations AI (free), Hugging Face, Stable Diffusion
- Automatic saving to Pictures folder
- High-quality, customizable outputs

#### PowerPoint Presentation Creator
- Generate complete presentations from topics
- AI-powered content creation using Google Gemini
- Multiple design themes: Professional, Modern, Dark
- Customizable slide counts (5-15 slides)
- Automatic formatting and styling

#### Code Generation
- Write complete code from voice descriptions
- Support for multiple languages: Python, JavaScript, Java, HTML, CSS, C++, C#
- Automatic VS Code integration
- Well-commented, production-ready code
- Intelligent syntax and best practices

### 📰 News & Information
- **Bilingual News**: English and Hindi news support
- **RSS Feed Integration**: Always-available news without API keys
- **News Categories**: Business, Sports, Technology, Entertainment, General
- **News Search**: Find articles on specific topics
- **Multiple Sources**: NDTV, The Hindu, India Today, BBC, Aaj Tak

### 📝 Productivity Tools
- **To-Do List Management**: Add, view, and delete tasks
- **Smart Reminders**: Set time-based reminders
- **Note Taking**: Create timestamped text notes
- **Folder Management**: Create and organize folders
- **Wikipedia Integration**: Quick information lookup

### 🌦️ Weather & Utilities
- Real-time weather information for any city
- Temperature, humidity, and wind speed details
- Current time and date announcements
- Internet speed testing
- System information reporting

### 🎯 Voice-First Design
- **Wake Word Activation**: Simply say "IRA" to start
- **Natural Language Processing**: Understand conversational commands
- **Context-Aware**: Maintains conversation flow
- **Error Handling**: Graceful fallbacks and helpful suggestions

## 🚀 Installation

### Prerequisites
```bash
Python 3.8 or higher
pip (Python package manager)
Microphone (for voice input)
Speakers (for voice output)
```

### Required Libraries
```bash
pip install eel
pip install SpeechRecognition
pip install gTTS
pip install pygame
pip install googletrans==4.0.0-rc1
pip install requests
pip install pyautogui
pip install speedtest-cli
pip install psutil
pip install pywin32  # Windows only
pip install winshell  # Windows only
pip install wikipedia
pip install python-pptx
pip install google-generativeai
pip install PyPDF2
pip install python-docx
pip install feedparser
pip install setuptools
pip install pyperclip
```

### Optional Dependencies
```bash
pip install pycaw  # For volume control on Windows
```

## 🎮 Usage

### Starting IRA
```bash
python main.py
```

The assistant will initialize and start listening for the wake word "IRA".

### Basic Commands

#### Language Commands
- "Change language to Hindi"
- "Switch language to Spanish"
- "List available languages"
- "Translate [text] to French"

#### System Control
- "Take a screenshot"
- "Increase volume"
- "Decrease brightness"
- "Check battery status"
- "Lock the PC"
- "Shutdown computer"
- "Restart system"

#### File Operations
- "Read file [filename]"
- "Read PDF [filename]"
- "Read Word document [filename]"
- "Create note"
- "Create folder [name]"

#### AI Features
- "Generate image of a sunset over mountains"
- "Create presentation on artificial intelligence"
- "Write code for a calculator in Python"
- "Make a website homepage"

#### Information & News
- "What's the weather in New York?"
- "Tell me the news"
- "Hindi news"
- "Search news about climate change"
- "Business news"
- "Sports headlines"

#### Network & System
- "What's my Wi-Fi password?"
- "Show network information"
- "Check internet speed"
- "Check disk usage on C drive"
- "Check CPU usage"

#### Productivity
- "Add task to buy groceries"
- "Show my tasks"
- "Set reminder for meeting at 14:30"
- "Search Wikipedia for Python programming"

## 🔧 Configuration

### API Keys (Optional)

The assistant works without API keys using RSS feeds and free services, but you can enhance functionality with:

#### Google Gemini AI (for advanced features)
```python
GEMINI_API_KEY = "your_api_key_here"
```
Get it from: https://makersuite.google.com/app/apikey

#### Weather API
```python
WEATHER_API_KEY = "your_api_key_here"
```
Get it from: https://openweathermap.org/api

#### News API (optional)
```python
NEWS_API_KEY = "your_api_key_here"
```
Get it from: https://newsapi.org/register

### Customization

#### Change Default Language
```python
CURRENT_LANGUAGE = "en"  # Change to your preferred language code
CURRENT_LANG_CODE = "en-in"
```

#### Modify File Paths
```python
# Notes location
notes_folder = Path.home() / "Documents" / "AssistantNotes"

# Code files location
code_dir = Path.home() / "Documents" / "IRA_Code_Files"

# Presentations location
ppt_folder = Path.home() / "Documents" / "IRA_Presentations"
```

## 📁 Project Structure

```
IRA/
├── main.py                 # Main assistant logic
├── engine/
│   └── features.py         # Additional features
├── web/
│   ├── index.html         # Web interface
│   ├── style.css          # UI styling
│   └── script.js          # Frontend logic
├── requirements.txt        # Python dependencies
└── README.md              # Documentation
```

## 🌐 Web Interface

IRA includes a modern web-based interface built with Eel that provides:
- Real-time conversation display
- Visual feedback for commands
- Message history
- Responsive design

Access at: `http://localhost:8080` (default port)

## 🔒 Privacy & Security

- All voice processing happens locally
- No data is sent to external servers (except for API calls)
- File operations are restricted to user directories
- Wi-Fi passwords are only retrieved with explicit commands

## ⚠️ Known Limitations

- Volume control requires `pycaw` on Windows
- Some system commands are Windows-specific
- VS Code must be installed for code generation features
- API rate limits apply for external services

## 🐛 Troubleshooting

### Microphone Not Working
```python
# Test microphone
import speech_recognition as sr
r = sr.Recognizer()
with sr.Microphone() as source:
    print("Say something...")
    audio = r.listen(source)
```

### Wake Word Not Detected
- Check microphone permissions
- Reduce background noise
- Speak clearly and at moderate volume
- Verify `speech_recognition` installation

### Module Not Found Errors
```bash
pip install --upgrade [module_name]
```

### API Errors
- Verify API keys are correct
- Check internet connection
- Ensure API quotas aren't exceeded

## 🤝 Contributing

Contributions are welcome! Please follow these steps:
1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👤 Creator

**Ankita Singh**
- LinkedIn: [Ankita Singh](https://www.linkedin.com/in/ankita-singh-932729309/)

## 🙏 Acknowledgments

- Google Gemini AI for advanced language processing
- Pollinations AI for free image generation
- NewsAPI and RSS feeds for news content
- Open-source community for various libraries

## 📞 Support

For issues, questions, or suggestions:
- Open an issue on GitHub
- Connect on LinkedIn: [Ankita Singh](https://www.linkedin.com/in/ankita-singh-932729309/)

## 🔮 Future Enhancements

- [ ] Smart home device integration
- [ ] Calendar and email management
- [ ] Advanced conversation memory
- [ ] Mobile app version
- [ ] Plugin system for extensions
- [ ] Voice customization options
- [ ] Multi-user support

---

**Made with ❤️ by Ankita Singh**

*IRA - Your Personal AI Assistant in Your Language*
