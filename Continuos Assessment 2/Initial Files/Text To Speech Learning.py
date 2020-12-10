import win32com.client as wincl
speak = wincl.Dispatch("SAPI.SpVoice")
speak.Speak("Hello World")


import pyttsx3
engine = pyttsx3.init()
engine.say("I will speak this text")
engine.runAndWait()
