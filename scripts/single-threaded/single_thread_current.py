"""
-------------------------------------------------------------------------------------
*******           TABLEAU WEB SERVICES (OPENWEATHER API)           *******

Request current weather data from the OpenWeather API via Table Extensions.

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
import requests
import pandas as pd

def current_weather(cities, api_key):
  # gets current weather data for the specified geolocation
  def rest_current(api_key, cities):
    # a list of current weather data per city
    city_data = {}
    # iterate through the cities dict
    for city in cities:
      # assign coordinate
      name = city["city"]
      lon = city["lon"]
      lat = city["lat"]
      parameters = f'lat={lat}&lon={lon}&appid={api_key}&units=imperial'
      url = f'https://api.openweathermap.org/data/2.5/weather?{parameters}'
      response = requests.get(url)
      payload = response.json()
      city_data[name] = payload
    return city_data

  # creates a dataframe from the JSON payload with current weather
  def transform_current(city_data):
    weather_data = pd.DataFrame()
    index = 0
    for city in city_data:
      index = index + 1
      # coordinates
      coord = city_data[city]["coord"]
      coord["ID"] = index
      coord = pd.DataFrame.from_dict([coord])

      # weather results
      weather = city_data[city]["weather"][0]
      del weather["id"]
      weather["ID"] = index
      weather = pd.DataFrame.from_dict([weather])

      # main weather data
      main = city_data[city]["main"]
      if "sea_level" in main:
        del main["sea_level"]
      if "grnd_level" in main:
        del main["grnd_level"]
      main["ID"] = index
      main = pd.DataFrame.from_dict([main])

      # visibility 
      visibility = {}
      visibility["visibility"] = city_data[city]["visibility"]
      visibility["ID"] = index
      visibility = pd.DataFrame.from_dict([visibility])

      # wind
      wind = {}
      wind["wind speed"] = city_data[city]["wind"]["speed"]
      wind["wind deg"] = city_data[city]["wind"]["deg"]
      wind["ID"] = index
      wind = pd.DataFrame.from_dict([wind])

      # clouds
      clouds = {}
      clouds["clouds"] = city_data[city]["clouds"]["all"]
      clouds["ID"] = index
      clouds = pd.DataFrame.from_dict([clouds])

      # country
      country = {}
      country["country"] = city_data[city]["sys"]["country"]
      country["ID"] = index
      country = pd.DataFrame.from_dict([country])

      # name (city)
      name = {}
      name["name"] = city_data[city]["name"]
      name["city_id"]= city_data[city]["id"]
      name["ID"] = index
      name = pd.DataFrame.from_dict([name])

      # joins the dataframes into a single row of data
      data = pd.merge(coord, weather, left_on='ID', right_on='ID', sort=False)
      data = pd.merge(data, main, left_on='ID', right_on='ID', sort=False)
      data = pd.merge(data, visibility, left_on='ID', right_on='ID', sort=False)
      data = pd.merge(data, wind, left_on='ID', right_on='ID', sort=False)
      data = pd.merge(data, clouds, left_on='ID', right_on='ID', sort=False)
      data = pd.merge(data, country, left_on='ID', right_on='ID', sort=False)
      data = pd.merge(data, name, left_on='ID', right_on='ID', sort=False)

      # append data to weather_data as we iterate through each city
      weather_data = pd.concat([weather_data, data], ignore_index=True)

    # generates a dictionary where each key contains a list of values as required by Tableau
    weather_data.set_index('ID', drop=True, inplace=True)
    weather_data = weather_data.to_dict('list')

    return weather_data

  # workflow: 1. rest calls, 2. transform data, 3. return transformed data
  payload = rest_current(api_key, cities)
  current_weather_data = transform_current(payload)
  return current_weather_data

"""
uncomment the following assignments and return statement to run this script as a Tabpy function.
change this to a hardcoded API key or set an environment variable in your Tabpy environment.
"""
#api_key = "API_KEY"
##creates a dataframe of cities from the input table (.csv file)
#cities_df = pd.DataFrame(_arg1)
##converts the dataframe to a dict with records orient
#cities = cities_df.to_dict('records')
#return current_weather(cities,api_key)

"""
-------------------------------------------------------------------------------------
Table Extension script ends here
-------------------------------------------------------------------------------------
"""

api_key = env_dict["API_KEY"]
# reads the .csv files containing a list of cities
cities_df = pd.read_csv('cities.csv', header=[0])
# converts the dataframe to a dict with records orient
cities = cities_df.to_dict('records')

# print the resulting dataset as a dataframe for readability
print(pd.DataFrame(current_weather(cities,api_key)))
# print(current_weather(cities))
