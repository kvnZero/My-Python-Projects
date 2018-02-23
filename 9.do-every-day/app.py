import requests
import json
session = requests.session()

def xixunyun_playcard():
    #wait..
    pass

def today_weather(city_id):
    API_KEY = "svbgsoto2mk6fvna"
    USER_ID = "U90560AB9B"
    for city in city_id:
        url = "https://api.seniverse.com/v3/weather/now.json?key=svbgsoto2mk6fvna&location=%s&language=zh-Hans&unit=c" % city
        json_text = session.get(url).text
        print(json_text)

def main():
    today_weather(['W7VHZEYSJ2W6'])

if __name__ == "__main__":
    main()