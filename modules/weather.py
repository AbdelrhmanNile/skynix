from pyowm import OWM
import os
import json

config = json.load(open(f"/home/{os.getlogin()}/skynix/config.json"))
owm = OWM(config["openweathermap_token"])
mgr = owm.weather_manager()


def get_weather(city: str):
    observation = mgr.weather_at_place(city)
    w = observation.weather
    status = w.detailed_status
    temp = w.temperature('celsius')['temp']
    return status, temp