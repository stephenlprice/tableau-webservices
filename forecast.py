"""
-------------------------------------------------------------------------------------
*******           TABLEAU WEB SERVICES (OPENWEATHER API)           *******

Request 5 day weather forecast data from the OpenWeather API via Table Extensions.

Table Extension scripts are essentially functions with a return statement. 
However, in order to support local development the final script is wrapped 
by certain imports and functions that can output results to a shell without
resulting in: (SyntaxError: 'return' outside function)

To deploy this code via a Table Extension, only copy the code marked
for usage in Tabpy and exclude any of the code used for local development.

To secure the necessary API key, use a .env file (see README.md) during local
development. This avoids pushing your key to public repositories such as Github.
When deployed to a Table Extension you can hardcode the API key in the script or
add it as an environment variable on the Tabpy Server.
-------------------------------------------------------------------------------------
"""

# imports used for local development
import os
from dotenv import load_dotenv

# load environment files from .env
load_dotenv(".env")
# calling environ is expensive, this saves environment variables to a dictionary
env_dict = dict(os.environ)

env_api_key = env_dict["API_KEY"]

"""
-------------------------------------------------------------------------------------
Table Extension script starts here
-------------------------------------------------------------------------------------
"""
# imports used by the Tabpy Function
import pandas as pd
from concurrent.futures import ThreadPoolExecutor
from requests_futures.sessions import FuturesSession

def current_weather(cities):
  """
  change this to a hardcoded API key or set an environment variable in your Tabpy environment
  """
  api_key = env_api_key

  # gets current weather data for the specified geolocation
  def rest_current(api_key, cities):
    # a list of current weather data per city
    city_data = {}

    # session object with python 3.2's concurrent.futures allowing for async requests
    session = FuturesSession(executor=ThreadPoolExecutor(max_workers=6))

    for city in cities:
      # assign coordinate
      name = city["city"]
      lon = city["lon"]
      lat = city["lat"]
      parameters = f'lat={lat}&lon={lon}&appid={api_key}&units=imperial'
      url = f'https://api.openweathermap.org/data/2.5/forecast?{parameters}'

      # futures are run in the background and are non-blocking
      future = session.get(url)
      # catching the returned future, .result() returns the response
      result = future.result()
      # response is serialized into json and inserted into the dict
      payload = result.json()
      city_data[name] = payload

    return city_data

  # creates a dataframe from the JSON payload with current weather
  def transform_current(city_data):
    weather_data = pd.DataFrame()
    index = 0
    for city in city_data:
      index = index + 1

      # location
      location = {}
      location["city_id"]= city_data[city]["id"]
      location["name"]= city_data[city]["name"]
      location["country"]= city_data[city]["country"]
      location["lat"]= city_data[city]["lat"]
      location["lon"]= city_data[city]["lon"]
      location = pd.DataFrame.from_dict(location)

      # payload per city contains a list with 5 day forecast every 3 hours
      forecasts = city_data[city]["list"]

      for forecast in forecasts:
        # timestamp and unix epoch
        time = {}
        time["timestamp"] = forecast["dt_txt"]
        time["unix_epoch"] = forecast["dt"]
        time["ID"] = index
        time = pd.DataFrame.from_dict(time)

        # main
        main = forecast["main"]
        if "sea_level" in main:
          del main["sea_level"]
        if "grnd_level" in main:
          del main["grnd_level"]
        main["ID"] = index
        main = pd.DataFrame.from_dict([main])

        # weather
        weather = forecast["weather"][0]
        if "id" in weather:
          del weather["id"]
        weather["clouds"] = forecast["clouds"]["all"]
        weather["ID"] = index
        weather = pd.DataFrame.from_dict([weather])

        # wind
        wind = forecast["wind"]
        wind["ID"] = index
        wind = pd.DataFrame.from_dict(wind)

        # visibility
        visibility = forecast["visibility"]
        visibility["ID"] = index
        visibility = pd.DataFrame.from_dict(visibility)

        # rain
        rain = {}
        if "rain" not in weather:
          rain["rain"] = 0
        else:
          rain["rain"] = visibility = forecast["rain"]["3h"]
        rain["ID"] = index
        rain = pd.DataFrame.from_dict(rain)


        # print(f'time: {time}')

    return weather_data

  payload = rest_current(api_key, cities)
  current_weather_data = transform_current(payload)

  return current_weather_data

"""
uncomment the following assignments and return statement to run this script as a Tabpy function
"""
##creates a dataframe of cities from the input table (.csv file)
#cities_df = pd.DataFrame(_arg1)
##converts the dataframe to a dict with records orient
#cities = cities_df.to_dict('records')
#return current_weather(cities)


"""
-------------------------------------------------------------------------------------
Table Extension script ends here
-------------------------------------------------------------------------------------
"""

# reads the .csv files containing a list of cities
cities_df = pd.read_csv('cities.csv', header=[0])
# converts the dataframe to a dict with records orient
cities = cities_df.to_dict('records')

print(current_weather(cities))
