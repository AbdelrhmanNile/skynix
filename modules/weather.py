from pyowm import OWM
from dotenv import load_dotenv
import os

load_dotenv("/home/pirate/git/skynix/.env")
owm = OWM(os.getenv("owm_api"))
mgr = owm.weather_manager()


def get_weather(city: str):
    observation = mgr.weather_at_place(city)
    w = observation.weather
    status = w.detailed_status
    temp = w.temperature('celsius')['temp']
    return status, temp