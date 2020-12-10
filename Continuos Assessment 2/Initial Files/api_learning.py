#default_city = "Exeter"
from flask import Flask,render_template,request
import os
import requests
import json
#app = Flask(__name__)



def weather():
    #global default_city
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    api_key = "<78b12252aa36eaeffc2aa2987edd68b7>"
    city_name = input("Enter city name : ")
    complete_url = base_url + "appid=" + "78b12252aa36eaeffc2aa2987edd68b7" + "&q=" + city_name
    # print response object
    response = requests.get(complete_url)
    x = response.json()
    if x["cod"] != "404":
        y = x["main"]
        current_temperature = y["temp"]
        current_pressure = y["pressure"]
        current_humidiy = y["humidity"]
        z = x["weather"]
        weather_description = z[0]["description"]
        # print following values
        weather_info = (" Temperature (in kelvin unit) = " +
        str(current_temperature) +
        "\n atmospheric pressure (in hPa unit) = " +
        str(current_pressure) +
        "\n humidity (in percentage) = " + str(current_humidiy) +
        "\n description = " + str(weather_description))
        print(weather_info)
#weather()

def news():
    url = "https://newsapi.org/v2/top-headlines?country=us&category=business&apiKey=857ae58dbaaf44efbf70504d75529a4c"
    #url = "https://newsapi.org/v2/top-headlines?source=bbc-news&apiKey=857ae58dbaaf44efbf70504d75529a4c"
    content = requests.get(url)
    news_contents = content.json()
    if news_contents["status"] == "ok":
        if news_contents["totalResults"] > 0:
            news_article = news_contents["articles"]
            for article in news_article:
                print(article["title"])
                print(article["urlToImage"])
                print(article["url"])
                break
        else:
            return []
    else:
        return []
    
news()

    


#if __name__ == "__main__":
    #app.run(debug = True,use_reloader = True)
