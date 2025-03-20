"""
pten.notice
~~~~~~~~~~~~

This module implements the notice functions.

"""

from . import logger
from .keys import Keys
from apscheduler.schedulers.blocking import BaseScheduler
import datetime
from lunardate import LunarDate
from openai import OpenAI
import requests
import json


class Notice:
    def __init__(self):
        self.report_func = print
        self.scheduler: BaseScheduler = None

    def set_report_func(self, func):
        self.report_func = func

    def set_scheduler(self, scheduler: BaseScheduler):
        self.scheduler = scheduler

    def report_text(self, text):
        self.report_func(text)


class Birthday(Notice):
    def __init__(self):
        super().__init__()

    @staticmethod
    def get_date_str_from_lunar_date(
        lunar_year, lunar_month, lunar_day, hour=8, minute=3, is_leap_month=False
    ):
        lunar_date = LunarDate(lunar_year, lunar_month, lunar_day, is_leap_month)
        solar_date = lunar_date.toSolarDate()
        return f"{solar_date} {hour:02d}:{minute:02d}:00"

    @staticmethod
    def is_leap_month(lunar_year, lunar_month):
        return lunar_month == LunarDate.leapMonthForYear(lunar_year)

    @staticmethod
    def get_now_lunar_date():
        now_solar_date = datetime.datetime.now()
        year = now_solar_date.year
        month = now_solar_date.month
        day = now_solar_date.day
        now_lunar_date = LunarDate.fromSolarDate(year, month, day)
        return now_lunar_date

    @staticmethod
    def generate_birthday_greeting(who, greeting_words=None):
        msg = f"今天是{who}的生日，让我们来祝福{who}吧"
        if greeting_words:
            msg = f"今天是{who}的生日，{greeting_words}"

        return msg

    def _add_lunar_schedule(
        self, msg, lunar_year, lunar_month, lunar_day, hour, minute
    ):
        run_date = self.get_date_str_from_lunar_date(
            lunar_year, lunar_month, lunar_day, hour, minute, False
        )
        args = [msg, lunar_month, lunar_day, hour, minute]
        func = self.report_lunar_birthday
        self.scheduler.add_job(func, "date", run_date=run_date, args=args)

        # solve leap month
        if not self.is_leap_month(lunar_year, lunar_month):
            return
        run_date = self.get_date_str_from_lunar_date(
            lunar_year, lunar_month, lunar_day, hour, minute, True
        )
        self.scheduler.add_job(func, "date", run_date=run_date, args=args)

    def _add_solar_schedule(self, msg, year, month, day, hour, minute):
        solar_date = datetime.date(year, month, day)
        run_date = f"{solar_date} {hour:02d}:{minute:02d}:00"
        args = [msg, month, day, hour, minute]
        func = self.report_solar_birthday
        self.scheduler.add_job(func, "date", run_date=run_date, args=args)

    def report_lunar_birthday(self, msg, lunar_month, lunar_day, hour=8, minute=3):
        self.report_func(msg)

        if self.scheduler is None:
            return

        # add next year's schedule job
        now_lunar_date = self.get_now_lunar_date()
        self._add_lunar_schedule(
            msg, now_lunar_date.year + 1, lunar_month, lunar_day, hour, minute
        )

    def report_solar_birthday(self, msg, month, day, hour=8, minute=3):
        self.report_func(msg)

        if self.scheduler is None:
            return

        # add next year's schedule job
        today = datetime.date.today()
        next_year = today.year + 1
        self._add_solar_schedule(msg, next_year, month, day, hour, minute)

    def add_lunar_schedule(
        self,
        lunar_month,
        lunar_day,
        hour=8,
        minute=3,
        who="someone",
        greeting_words=None,
    ):
        if self.scheduler is None:
            logger.error("Scheduler is not set. Please set_scheduler() first.")
            return

        msg = self.generate_birthday_greeting(who, greeting_words)

        now_lunar_date = self.get_now_lunar_date()
        lunar_date = LunarDate(now_lunar_date.year, lunar_month, lunar_day)
        if lunar_date < LunarDate.today():
            lunar_date = LunarDate(now_lunar_date.year + 1, lunar_month, lunar_day)

        self._add_lunar_schedule(
            msg, lunar_date.year, lunar_month, lunar_day, hour, minute
        )

    def add_solar_schedule(
        self, month, day, hour=8, minute=3, who="someone", greeting_words=None
    ):
        if self.scheduler is None:
            logger.error("Scheduler is not set. Please set_scheduler() first.")
            return

        msg = self.generate_birthday_greeting(who, greeting_words)

        now = datetime.datetime.now()
        solar_date = datetime.date(now.year, month, day)
        if solar_date < now.date():
            solar_date = solar_date.replace(year=now.year + 1)

        self._add_solar_schedule(msg, solar_date.year, month, day, hour, minute)


class Deepseek(Notice):
    def __init__(self, keys_filepath="pten_keys.ini", **kwargs):
        super().__init__()
        self.keys = Keys(keys_filepath)
        sk_api_key = self.keys.get_key("ai", "deepseek_api_key")
        self.deepseek_client = OpenAI(
            api_key=sk_api_key,
            base_url="https://api.deepseek.com",
        )

    def get_completion(self, prompt):
        response = self.deepseek_client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": "You are a helpful assistant"},
                {"role": "user", "content": prompt},
            ],
            stream=False,
        )

        return response.choices[0].message.content


class Weather(Notice):
    def __init__(self, keys_filepath="pten_keys.ini", **kwargs):
        super().__init__()
        self.keys = Keys(keys_filepath)
        self.api_key = self.keys.get_key("weather", "seniverse_api_key")
        self.cities = {}

    def add_city(self, city_name, city_code):
        self.cities[city_name] = city_code

    def get_weather(self, city_code):
        url = f"https://api.seniverse.com/v3/weather/now.json?key={self.api_key}&location={city_code}&language=zh-Hans&unit=c"

        response = requests.get(url)
        weather_json = json.loads(response.text)
        weather = weather_json["results"][0]["now"]

        return weather

    def get_city_weather(self, city_name, city_code):
        weather = self.get_weather(city_code)

        weather_text = weather.get("text")
        weather_temperature = weather.get("temperature")

        weather_str = f"{city_name}: {weather_text},\t 温度: {weather_temperature}度"

        return weather_str

    def report_weather(self):
        if not self.cities:
            logger.warning("No city added. Please add_city() first.")
            return
        weather_str = "今日天气："
        for city_name, city_code in self.cities.items():
            weather_str += "\n" + self.get_city_weather(city_name, city_code)

        self.report_func(weather_str)
