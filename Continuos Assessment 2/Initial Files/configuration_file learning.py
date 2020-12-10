import json
def config_handle():
    api = {}
    api["key"] = {
        "news": "857ae58dbaaf44efbf70504d75529a4c",
        "weather": "<78b12252aa36eaeffc2aa2987edd68b7>"
        }
    config_file = json.dumps(api)
    return config_file
    

def news_config(config_handle):
    data_file = config_handle()
    config_data = json.loads(data_file)
    news_api = config_data["key"]["news"]
    #print(news_api)
    return news_api
news_config(config_handle)

def weather_api(config_handle):
    data_file = config_handle()
    config_data = json.loads(data_file)
    weather_api = config_data["key"]["weather"]
    #print(weather_api)
    return weather_api
weather_api(config_handle)
    

base_url = "https://newsapi.org/v2/top-headlines?country=us&category=business&apiKey=857ae58dbaaf44efbf70504d75529a4c"

complete_url ="https://newsapi.org/v2/top-headlines?country=us&category=business&apiKey=" + news_config(config_handle)

if complete_url == base_url:
    print(True)
