from flask import Flask
from flask import request
app = Flask(__name__)

@app.route("/welcome_page")
def alarm_choice():
    return '<a href=/welcome_page>CREATE</a><a href=/create_alarm> ALARM</a>'
    return '<a href=/welcome_page>ALARM</a><a href=/cancel_alarm> CANCEL</a>'

@app.route("/create_alarm")
def create_alarm():
    return "Create Alarm"

@app.route("/cancel_alarm")
def cancel_alarm():
    return "Cancel Alarm"





if __name == "__main__":
    app.run()
