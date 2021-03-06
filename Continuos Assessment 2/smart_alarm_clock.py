"""SMART ALARM CLOCK PROGRAM """
import time
import json
from datetime import datetime, date
import sched
from flask import Flask, render_template, request
#import requests
#import pyttsx3

#2D List of Alarms
#Each list contains, date, time and reason
alarm_schedule = []
notified_alarms = []


app = Flask(__name__)


def config_handle() -> str:
    """This function opens a json file
       ,which is a configuration file, in
       read mode. The contents of this
       configuration file is a dictionary
       containing api keys and system file
       paths. This dictionary is accessed
       from the file and stored under the
       variable 'data_file' which is returned
       at the end of the function."""

    #Opening JSON File
    #Storing contents of file under variable
    with open("config.json", "r") as file_details:
        data_file = json.load(file_details)
    return data_file


def news_config() -> str:
    """The function config_handle()
       is called and the contents that
       are returned are stored in the variable
       'config file'. This  is then appropriately
       parsed so the news api key is accessed.
       This is then returned at the end of the
       function."""

    #Accessing News Api Key
    config_file = config_handle()
    api_key = config_file["api_keys"]["news_key"]
    return api_key


def weather_config() -> str:
    """The function config_handle() is called
      and the contents that are returned are
      stored in the variable 'config file'.
      This is then appropriately parsed so the
      weather api key is accessed. This is then
      returned at the end of the function."""

    #Accessing Weather Api Key
    config_file = config_handle()
    api_key = config_file["api_keys"]["weather_key"]
    return api_key


def alarm_notify(alarm_output, alarm_date, alarm_time):
    """This function takes three arugments, which
       is the date for the alarm, time of the alarm
       and the reason for the alarm.
       This is the function that is run when the
       calculated time interval has taken place.
       The reason for the alarm entered by the user
       is spoken out using the text to speech.Then
       the arguments that have been passed to this
       function is added to a list, one_alarm, and then added
       to the passed_alarms list.This way the alarm can be
       viewed as a passed alarm. The one_alarm list
       is then searched for in alarm_schedule and then
       removed, so it can no longer be viewed as an upcoming
       alarm."""

    one_alarm = []
    #Text To Speech Notifications
    engine = pyttsx3.init()
    engine.say(alarm_output)
    engine.runAndWait()

    #appending Notifation Details to List
    one_alarm.append(alarm_date)
    one_alarm.append(alarm_time)
    one_alarm.append(alarm_output)
    notified_alarms.append(one_alarm)

    #Removing Notified Alarm From Schedule
    for every_list in alarm_schedule:
        if every_list == one_alarm:
            alarm_schedule.remove(every_list)


alarm_group = sched.scheduler(time.time, time.sleep)


@app.route("/", methods=["GET", "POST"])
def home() -> str:
    """This is the home page that controls the system inputs
        The function takes no python argumetns but loads request
       arguments called 'Alarm' and 'name' and consists of
       a series of buttons which will allow the user
       to navigate to through the various parts of
       the program.Also, this is where notifiations take place.
       The 2D list containing all the alarms, is iterated through.
       In each list the date is checked and compared with the date
       today. If they are equivalent,the list is checked to see if
       it has already been scheduled. If not, then the the seconds
       difference between the current time and the time in the list
       is calculated and the alarm is scheduled.
       The return statement uses a template called home.html. """
    alarm_group.run(blocking=False)
    while not alarm_group.empty():
        alarm_group.cancel(alarm_group.queue[0])
    #Getting Current Date
    current_date = str(date.today())
    #Getting Current Time
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    #Getting appropriate Times From List
    for interior_list in alarm_schedule:
        if interior_list[0] == current_date:
            time_format = "%H:%M:%S"
            user_time = interior_list[1] + ":00"
            first_time = datetime.strptime(user_time, time_format)
            second_time = datetime.strptime(current_time, time_format)
            time_difference = first_time - second_time
            if time_difference.days < 0:
                pass
            else:
                proper_difference = (time_difference.days *
                                     23 * 3600 + time_difference.seconds)
                alarm_date = interior_list[0]
                alarm_time = interior_list[1]
                alarm_output = interior_list[2]
                alarm_group.enter(proper_difference, 1, alarm_notify,
                                  argument=(alarm_output, alarm_date,
                                            alarm_time))
    #Accessing Template from JSON File
    config_file = config_handle()
    home_template = config_file["file_paths"]["home_page"]
    return render_template(home_template)

#Page where you can Create Alarms
@app.route("/create_alarm", methods=["GET", "POST"])
def create_page() -> str:
    """This function returns a singular html
       template. This template allows the user
       to enter the date,time and reason for an
       alarm to be created."""
    config_file = config_handle()
    create_template = config_file["file_paths"]["create_input"]
    return render_template(create_template)

#Page where you can Cancel Alarms
@app.route("/cancel_alarm", methods=["GET", "POST"])
def cancel_page() -> str:
    """This function allows the user to enter
       data so an alarm that had been previously
       scheduled could now be cancelled. Firstly
       each list in alarm_schedule is iterated
       through and each element in that list
       is added to a string. Then when each
       list had been iterated through the string
       was appended to a list called cancel_list.
       This was then passed to a template which is
       returned at the end. The template allowed
       the user interface to view all the alarms
       that had been currently scheduled and input
       date, time and reason of the alarm they would
       like to cancel."""
    #List of alarms that could be Cancelled
    cancel_list = []
    index_string = ""
    #Iterate through list of alarms
    for internal_list in alarm_schedule:
        index_string = ("Date: " + internal_list[0] +
                        "  Time: ", internal_list[1]
                        +"Reason: ", internal_list[2])
        cancel_list.append(index_string)

    #Accessing Template from JSON File
    config_file = config_handle()
    cancel_template = config_file["file_paths"]["cancel_input"]
    return render_template(cancel_template, cancel_options=cancel_list)


#Page where you can Enter City
@app.route("/weather_input", methods=["GET", "POST"])
def weather_page() -> str:
    """This function returns a single html template.
       The function allows the program to ask the
       user to enter the name of a city, based on
       this input a json file will be parsed and
       the appropriate information will be displayed"""

    #Accessing Template from JSON File
    config_file = config_handle()
    weather_template = config_file["file_paths"]["weather_input"]
    return render_template(weather_template)


#Processes details entered by the user about alarm created
#Confirms to the user that the alarm has been created
@app.route("/create_process", methods=["GET", "POST"])
def create_alarm() -> str:
    """This function takes the data the user has
       inputted to create an alarm. Firstly it
       splits the datetime entered by the user into
       a date and a time and then appends these and
       the, reason for the alarm entered by the user,
       into a list. It then appends this list to another
       list where all the existing alarms are. The details
       about the alarm are then passed to the template that
       are returned at the end. The templates allows the
       user interface to display details about the alarm
       so the program confirms to the user exactly what
       they have scheduled."""
    #List space for just one alarm
    schedule_section = []

    #Catches date and time user has entered
    user_date_time = request.args.get("date_time")
    #Catches reason user has entered
    user_reason = request.args.get("reason")

    #Seperates date and time
    analyse_list = list(user_date_time)
    alarm_date = ""
    alarm_time = ""
    for date_part in range(0, 10):
        alarm_date = alarm_date + analyse_list[date_part]
    for time_part in range(11, 16):
        alarm_time = alarm_time + analyse_list[time_part]

    #appends information to a list
    schedule_section.append(alarm_date)
    schedule_section.append(alarm_time)
    schedule_section.append(user_reason)

    #appends list to the overall alarm list
    alarm_schedule.append(schedule_section)

    #Outputs Alarm created by the user
    confirm_message = ("Alarm created at", alarm_time, "on",
                       alarm_date, "because of", user_reason)

    #Accessing Template from JSON File
    config_file = config_handle()
    create_template = config_file["file_paths"]["create_output"]
    return render_template(create_template,
                           user_confirm=confirm_message)

#Process data entered by the user
#So program can cancel alarm
@app.route("/cancel_process", methods=["GET", "POST"])
def cancel_alarm() -> str:
    """This function firstly catches the datetime
       and reason entered by the user of the alarm
       they would like to cancel. The datetime caught
       is split into a date and a time.Then alarm_schedule
       is iterated through to find a list that contains
       the same date,time and reason. If this is found the
       list is removed and a message of success is passed to
       the template. Otherewise an error message is passed
       to the template that is returned at the end. The templates
       allows the user interface to display whether the user
       had been successful in cancelling their alarmor not."""
    #Catches date and time entered by the user
    cancel_date_time = request.args.get("date_time")
    #Catches reason entered by the user
    cancel_reason = request.args.get("reason")

    #Seperates date and time entered by the user
    inspect_list = list(cancel_date_time)
    cancel_date = ""
    cancel_time = ""
    for date_piece in range(0, 10):
        cancel_date = cancel_date + inspect_list[date_piece]
    for time_piece in range(11, 16):
        cancel_time = cancel_time + inspect_list[time_piece]

    #Searches through the list of alarms
    #For the alarm entered by the user
    for inner_list in alarm_schedule:
        if inner_list[0] == cancel_date:
            if inner_list[1] == cancel_time:
                if inner_list[2] == cancel_reason:
                    alarm_schedule.remove(inner_list)
                    cancel_message = "Alarm Removed"
                    print(alarm_schedule)
                else:
                    cancel_message = "Error: Reason Not Recognised"
            else:
                cancel_message = "Error: Time Not Recognised"
        else:
            cancel_message = "Error: Date Not Recognised"

    #Accessing Template from JSON File
    config_file = config_handle()
    cancel_template = config_file["file_paths"]["cancel_output"]
    return render_template(cancel_template
                           , display_message=cancel_message)


#Lets user view all Upcoming Alarms
@app.route("/view_alarm", methods=["GET", "POST"])
def view_alarm() -> str:
    """This function allows the user to view all
       the upcoming alarms in currently in the
       schedule. To allow the user to be able to
       see this in an appropriate way, each list in
       alarm_schedule is iterated through. Each element
       in the list is added to a string and then that
       string is added to a list called alarms. Then
       the list alarms is passed to the template
       view_alarm which is returned in the end. In the
       template the each element in alarms is displayed
       so each alarm can be viewed easily by the user."""

    #Iterating through list of Alarms
    alarms = []
    for inside_list in alarm_schedule:
        alarm_string = ""
        alarm_string += ("Date: " + inside_list[0] + " Time: "
                         + inside_list[1] + " Reason: " + inside_list[2])
        alarms.append(alarm_string)

    #Accessing Template from JSON File
    config_file = config_handle()
    view_template = config_file["file_paths"]["upcoming_alarm"]
    return render_template(view_template, display_list=alarms)

#Lets user view all Passed Alarms
@app.route("/view_notifications", methods=["GET", "POST"])
def passed_alarms() -> str:
    """This function allows the user to view all alarms that
       have already been notified to the the user. When an
       alarm is notfied to the user by the program, the date,
       time and reason for the alarm is added to a list which
       is added to another list containing all the notified
       alarms. In this function every lists in there is
       iterated through and every element to the list is added
       a string. Every string created is added a list called
       passed_display. This is then passed to the template
       view_notifcations, which is returned at the end.
       In this tempalte, every element in passed_display is
       outputted so the user can view all the passed alarms."""

    #Iterating through list of Notified Alarms
    passed_display = []
    for interior_array in notified_alarms:
        notification_string = ""
        notification_string += ("Date: " + interior_array[0] + " Time: "
                                + interior_array[1] + " Reason: " + interior_array[2])
        passed_display.append(notification_string)

    #Accessing Template from JSON File
    config_file = config_handle()
    view_template = config_file["file_paths"]["passed_alarm"]
    return render_template(view_template,
                           display_alarms=passed_display)

#Processes city entered by the user
#So relevant information is displayed to the user
@app.route("/display_weather", methods=["GET", "POST"])
def weather_display() -> str:
    """This function catches the city entered by the user
       and outputs the current weather information relevant
       to the city entered by the user. Firstly the weather_config
       function is called so the weather api key is produced and
       added to the url. Based on thsi url a request is made so some
       JSON data can be produced. This JSON data is parsed so the
       relevant information about weather in the city is produced.
       This is then added to a the list info_list. This is then
       the passed to the tempalte display_weather, which is returned
       at the end of the function. In this template every element in
       info_list is outputted so the user can see the weather
       information about the city the user entered."""

    #Formation of URL
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    api_key = weather_config()
    city_name = str(request.args.get("user_city"))
    complete_url = base_url + "appid=" + api_key + "&q=" + city_name

    #Request of JSON Data
    response = requests.get(complete_url)
    response_data = response.json()

    #Parsing of JSON Data
    if response_data["cod"] != "404":
        weather_data = response_data["main"]
        current_temperature = weather_data["temp"]
        current_pressure = weather_data["pressure"]
        current_humidiy = weather_data["humidity"]
        specific_data = response_data["weather"]
        weather_description = specific_data[0]["description"]

    #Making Data Easier to View
    info_list = []
    info_list.append(" Temperature (in kelvin unit) = " + str(current_temperature))
    info_list.append(" Atmospheric Pressure (in hPa unit) = " + str(current_pressure))
    info_list.append(" Humidity (in percentage) = " + str(current_humidiy))
    info_list.append(" Description = " + str(weather_description))

    #Accessing Template from JSON File
    config_file = config_handle()
    weather_template = config_file["file_paths"]["weather_output"]
    return render_template(weather_template, display_info=info_list)

@app.route("/display_news", methods=["GET", "POST"])
def news_display() -> str:
    """This is the function that is ran when the
       'latest news' button is pressed. The function
        calls the news_config function to access
        the news api key. This is then used to form
        an URL where this can be requested so JSON
        data can be accessed. This JSON data can be
        parsed, so the title,image and URL for the
        news article is accessed. This is then added
        to a list which is passed to the template
        display_news which is returned at the end.
        In this tepalte every element is outputted."""
    news_collection = []

    #Formation of URL
    base_url = ("https://newsapi.org/v2/top-headlines?country="+
                "us&category=business&apiKey=")
    api_key = news_config()
    complete_url = base_url + api_key
    content = requests.get(complete_url)

    #Request and Parsing of JSON Data
    news_contents = content.json()
    if news_contents["status"] == "ok":
        if news_contents["totalResults"] > 0:
            news_article = news_contents["articles"]
            for article in news_article:
                news_collection.append(article["title"])
                news_collection.append(article["urlToImage"])
                news_collection.append(article["url"])
                break
        else:
            return "Error: Data Not Found"
    else:
        return "Error: Data Not Found"

    #Accessing Template from JSON File
    config_file = config_handle()
    news_template = config_file["file_paths"]["news_output"]
    return render_template(news_template, news_title=news_collection[0],
                           image_link=news_collection[1], news_link=news_collection[2])


if __name__ == "__main__":
    app.run(debug=True, use_reloader=True)
