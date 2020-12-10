#New Imports Required
import sched
from sched import scheduler
from datetime import datetime
from datetime import date
import time
##import win32com.client as wincl
import pyttsx3

#Imports Already There
from flask import Flask,render_template,request,flash,redirect,url_for
from datetime import datetime
import os
import requests





app = Flask(__name__)

#@app.route("/notify",methods = ["GET","POST"])
def alarm_notify(alarm_output):
    print(alarm_output, flush=True)
##    speak = wincl.Dispatch("SAPI.SpVoice")
##    speak.Speak(alarm_output)
    engine = pyttsx3.init()
    engine.say(alarm_output)
    engine.runAndWait()

alarm_group = sched.scheduler(time.time,time.sleep)

@app.route("/",methods = ["GET","POST"])
def alarm_formation():
    alarm_group.run(blocking=False)
    #Getting Current Date
    current_date = str(date.today())
    print(current_date)
    #Getting Current Time
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print("Current Time: ",current_time)
    #Getting Appropriate Times From List
    schedule = [["2019-11-23","10:30:00","wake up"],["2019-11-14","18:30:00","dinner time"],["2019-11-14","18:31:00","washing up"]]
    FMT = '%H:%M:%S'
    for interior_list in schedule:
        if interior_list[0] == current_date:
            time_difference = datetime.strptime(interior_list[1], FMT) - datetime.strptime(current_time, FMT)
            if time_difference.days < 0:
                pass
            else:
                proper_difference = time_difference.days * 23 * 3600 + time_difference.seconds
                print(proper_difference)
                alarm_output = interior_list[2]
                alarm_group.enter(proper_difference,1,alarm_notify,argument = (alarm_output,))
                print("Hello")
                #alarm_group.run(blocking = False)
    return render_template("spare_stuff.html")
#alarm_formation()
    


if __name__ == "__main__":
    app.run(debug = False,use_reloader = False)

        

