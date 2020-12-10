import json

def dump_data():
    config_data = { "api_keys":{
        "news_key": "857ae58dbaaf44efbf70504d75529a4c",
        "weather_key": "78b12252aa36eaeffc2aa2987edd68b7"
                    },
         "file_paths":{           
        "home_page": "home.html",
        "cancel_input":"cancel_alarm.html",
        "weather_input":"weather_input.html",
        "create_input": "create_alarm.html",
        "cancel_output":"cancel_confirm.html",
        "create_output":"create_confirm.html",
        "upcoming_alarm":"view_alarm.html",
        "passed_alarm":"view_notifications.html",
        "weather_output":"display_weather.html",
        "news_output":"display_news.html"}
        }
    with open("config.json","w") as f:
        json.dump(config_data,f)

dump_data()


def config_handle():
    with open("config.json","r") as f:
        data_file = json.load(f)
    api_key = data_file["api_keys"]["weather_key"]
    html_template = data_file["file_paths"]["home_page"]
    print(html_template)
    print(api_key)
config_handle()
