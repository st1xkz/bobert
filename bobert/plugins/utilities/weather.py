import json
import os
from datetime import datetime
from math import trunc

import hikari
import lightbulb
import pytemperature

weather = lightbulb.Plugin("weather")


WEATHER_KEY = os.environ["WEATHER_KEY"]


def degtocompass(deg):
    val = int((deg / 22.5) + 0.5)
    arr = [
        "North (N)",
        "North-Northeast (NNE)",
        "Northeast (NE)",
        "East-Northeast (ENE)",
        "East (E)",
        "East-Southeast (ESE)",
        "Southeast (SE)",
        "South-Southeast (SSE)",
        "South (S)",
        "South-Southwest (SSW)",
        "Southwest (SW)",
        "West-Southwest (WSW)",
        "West (W)",
        "West-Northwest (WNW)",
        "Northwest (NW)",
        "North-Northwest (NNW)",
    ]
    return arr[(val % 16)]


def meter_km(meter):
    km = meter * 0.001
    trc = trunc(km)
    return trc


def mps_to_kmh(mtr):
    mul = mtr * 18
    div = mul / 5
    trc = trunc(div)
    return trc


def wind_condition(wind_speed):
    if wind_speed >= 0 and wind_speed <= 0.2:
        return "Calm"
    elif wind_speed >= 0.2 and wind_speed <= 1.5:
        return "Light Air"
    elif wind_speed >= 1.5 and wind_speed <= 3.3:
        return "Light Breeze"
    elif wind_speed >= 3.3 and wind_speed <= 5.4:
        return "Gentle Breeze"
    elif wind_speed >= 5.4 and wind_speed <= 7.9:
        return "Moderate Breeze"
    elif wind_speed >= 7.9 and wind_speed <= 10.7:
        return "Fresh Breeze"
    elif wind_speed >= 10.7 and wind_speed <= 13.8:
        return "Strong Breeze"
    elif wind_speed >= 13.8 and wind_speed <= 17.1:
        return "Near Gale"
    elif wind_speed >= 17.1 and wind_speed <= 20.7:
        return "Gale"
    elif wind_speed >= 20.7 and wind_speed <= 24.4:
        return "Severe Gale"
    elif wind_speed >= 24.4 and wind_speed <= 28.4:
        return "Strong Storm"
    elif wind_speed >= 28.4 and wind_speed <= 32.6:
        return "Violent Storm"
    elif wind_speed >= 32.6:
        return "Hurricane"


@weather.command
@lightbulb.add_cooldown(10, 3, lightbulb.UserBucket)
@lightbulb.option(
    name="city",
    description="the city to check",
    type=str,
    required=True,
    modifier=lightbulb.commands.OptionModifier.CONSUME_REST,
)
@lightbulb.command(
    name="weather",
    description="Look up the weather in a particular city",
    pass_options=True,
)
@lightbulb.implements(lightbulb.SlashCommand)
async def _weather(ctx: lightbulb.Context, city: str) -> None:
    try:
        params = {
            "q": city,
            "appid": WEATHER_KEY,
            "units": "metric",
        }
        async with ctx.bot.d.aio_session.get(
            "http://api.openweathermap.org/data/2.5/weather",
            params=params,
        ) as resp:
            data = json.loads(await resp.read())

        code = data["cod"]
        if code != 200:
            try:
                msg = data["message"]
                if code == 404:
                    await ctx.respond(
                        "City cannot be found! Please check your spelling and/or if it's a real city."
                    )
                elif code == 401:
                    raise ValueError("Invalid API Key!")
                else:
                    raise ValueError(
                        f"An Error Occured! '{msg.capitalize()}' (Code: '{code}')"
                    )
            except AttributeError:
                raise ValueError("Fatal Error Occured, Please try again later!")

        cityname = data["name"]
        countryid = data["sys"]["country"]
        status = data["weather"][0]["description"]
        sunrise = data["sys"]["sunrise"]
        sunset = data["sys"]["sunset"]
        timezone_offset = data["timezone"]
        clouds = data["clouds"]["all"]
        lon = data["coord"]["lon"]
        lat = data["coord"]["lat"]
        temp_c = data["main"]["temp"]
        feels_c = data["main"]["feels_like"]
        t_min_c = data["main"]["temp_min"]
        t_max_c = data["main"]["temp_max"]
        temp_f = pytemperature.c2f(temp_c)
        feels_f = pytemperature.c2f(feels_c)
        t_min_f = pytemperature.c2f(t_min_c)
        t_max_f = pytemperature.c2f(t_max_c)
        pressure = data["main"]["pressure"]
        humidity = data["main"]["humidity"]
        vis = data["visibility"]
        wind = data["wind"]["speed"]
        wind_degree = data["wind"]["deg"]
        wind_direction = degtocompass(wind_degree)

    except IndexError:
        raise ValueError("An error occurred while parsing the data.")
    except KeyError:
        raise ValueError("An error occurred while parsing the data.")
    colors = ""

    if temp_c > 36:
        colors = hikari.Color(0xFF0000)
    elif temp_c > 28:
        colors = hikari.Color(0xFFFF00)
    elif temp_c > 16:
        colors = hikari.Colour(0x26D935)
    elif temp_c > 8:
        colors = hikari.Colour(0x006BCE)
    elif temp_c > 2:
        colors = hikari.Colour(0xB4CFFA)
    elif temp_c <= 2:
        colors = hikari.Colour(0x0000FF)
    else:
        colors = hikari.Color(0x2F3136)
    calculated_sunrise = datetime.fromtimestamp(sunrise + timezone_offset)
    calculated_sunset = datetime.fromtimestamp(sunset + timezone_offset)

    embed = (
        hikari.Embed(
            title=f"Weather for {cityname}, {countryid} ~ {status}",
            color=colors,
            timestamp=datetime.now().astimezone(),
        )
        .add_field(
            "Current Temp",
            f"{temp_f}°F/{temp_c}°C",
            inline=True,
        )
        .add_field(
            "Feels like",
            f"{feels_f}°F/{feels_c}°C",
            inline=True,
        )
        .add_field(
            "Min Temp",
            f"{t_min_f}°F/{t_min_c}°C",
            inline=True,
        )
        .add_field(
            "Max Temp",
            f"{t_max_f}°F/{t_max_c}°C",
            inline=True,
        )
        .add_field(
            "Cloudiness",
            f"{clouds}%",
            inline=True,
        )
        .add_field(
            "Sunrise",
            f"{calculated_sunrise} (UTC)",
            inline=True,
        )
        .add_field(
            "Sunset",
            f"{calculated_sunset} (UTC)",
            inline=True,
        )
        .add_field(
            "Atmospheric Pressure",
            f"{pressure} hPa",
            inline=True,
        )
        .add_field(
            "Humidity",
            f"{humidity}%",
            inline=True,
        )
        .add_field(
            "Visibility",
            f"{vis} Meter ({meter_km(vis)} Km)",
            inline=True,
        )
        .add_field(
            "Wind Speed",
            f"{wind} m/sec | {mps_to_kmh(wind)} km/h ({wind_condition(wind)})",
            inline=True,
        )
        .add_field(
            "Wind Direction",
            f"{wind_degree}° {wind_direction}",
            inline=True,
        )
        .add_field(
            "Longitude",
            f"{lon}",
            inline=True,
        )
        .add_field(
            "Latitude",
            f"{lat}",
            inline=True,
        )
        .set_footer(
            text="Data provided by OpenWeatherMap.org",
        )
    )
    await ctx.respond(embed=embed)


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(weather)


def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(weather)
