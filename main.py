import os
import eel
from engine.features import *
from engine.command import *
from engine.command import allCommands, hotword_listener
from engine.auth import recoganize
from multiprocessing import Process
def start():

 eel.init("www")
 playAssistantSound()
 @eel.expose
 def init():
    # subprocess.call([r'device.bat'])
    eel.hideLoader()
    speak("Ready for Face Authentication...")
    flag=recoganize.AuthenticateFace()
    if flag==1:
      eel.hideFaceAuth()
      speak("Face Authentication Successsful!!")
      eel.hideFaceAuthSuccess()
      speak("Hello, Welcome")
      eel.hideStart()
      playAssistantSound()
    else:
      speak("Face Authentication Fail!!")
 os.system('start msedge.exe --app="http://localhost:8000/index.html"')
 eel.start('index.html',mode=None,host='localhost',block=True)
