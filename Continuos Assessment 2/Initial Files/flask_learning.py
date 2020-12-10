from flask import Flask
from flask import request
app = Flask(__name__)

@app.route("/")
def hello():
    alarm = request.args.get(alarm)
    if alarm:
        print(alarm)
    return '<form action = "/" method="get">\
        <input type="datetime-local" name="alarm">\
        <input type="submit"></form>'

##@app.route("/hello")
##def hello_world():
##    return '<a href=/hello>Hello</a><a href=/setalarm> alarm!</a>'
##
##@app.route("/setalarm")
##def alarm():
##    return '<a href=/setalarm> alarm!</a><a href=/hello>Hello</a>'

if __name__ == "__main__":
    app.run()
