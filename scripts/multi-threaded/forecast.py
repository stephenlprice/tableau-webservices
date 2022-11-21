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
import os, time
from dotenv import load_dotenv

# load environment files from .env
load_dotenv(".env")
# calling environ is expensive, this saves environment variables to a dictionary
env_dict = dict(os.environ)

"""
-------------------------------------------------------------------------------------
Table Extension script starts here
-------------------------------------------------------------------------------------
"""
# imports used by the Tabpy Function
import pandas as pd
from concurrent.futures import ThreadPoolExecutor
from requests_futures.sessions import FuturesSession

def forecast_weather(cities, api_key):
  forecast_df = pd.DataFrame()
  # gets weather forecast data for the specified geolocations
  def get_data(cities, api_key):
    # a dict of weather forecast data per city
    forecasts = {}
    # session object with python 3.2's concurrent.futures allowing for async requests
    session = FuturesSession(executor=ThreadPoolExecutor())
    for city in cities:
      # assign coordinate
      name = city["city"]
      lon = city["lon"]
      lat = city["lat"]
      query_parameters = f'lat={lat}&lon={lon}&appid={api_key}&units=imperial'
      url = f'https://api.openweathermap.org/data/2.5/forecast?{query_parameters}'
      # futures are run in the background and are non-blocking
      future = session.get(url)
      # catching the returned future, .result() returns the response
      result = future.result()
      # response is serialized into json and inserted into the dict
      payload = result.json()
      forecasts[name] = payload
    # create a single dataframe containing all forecasts
    processed_data = process(forecasts)
    # formats the dataframe into a dict for Tableau
    return output_table(processed_data)


  def process(forecasts):
    # each row will have a unique index
    index = 0
    for forecast in forecasts:
      forecast_list = forecasts[forecast]["list"]
      for forecast_3hr in forecast_list:
        index = index + 1
        # location
        location = {}
        location["city_id"]= forecasts[forecast]["city"]["id"]
        location["name"]= forecasts[forecast]["city"]["name"]
        location["country"]= forecasts[forecast]["city"]["country"]
        location["lat"]= forecasts[forecast]["city"]["coord"]["lat"]
        location["lon"]= forecasts[forecast]["city"]["coord"]["lon"]
        location["ID"] = index
        location = pd.DataFrame.from_dict([location])

        # timestamp and unix epoch
        time = {}
        time["timestamp"] = forecast_3hr["dt_txt"]
        time["unix_epoch"] = forecast_3hr["dt"]
        time["ID"] = index
        time = pd.DataFrame.from_dict([time])

        # main
        main = forecast_3hr["main"]
        if "sea_level" in main:
          del main["sea_level"]
        if "grnd_level" in main:
          del main["grnd_level"]
        main["ID"] = index
        main = pd.DataFrame.from_dict([main])

        # weather
        weather = forecast_3hr["weather"][0]
        if "id" in weather:
          del weather["id"]
        weather["clouds"] = forecast_3hr["clouds"]["all"]
        weather["ID"] = index
        weather = pd.DataFrame.from_dict([weather])

        # wind
        wind = forecast_3hr["wind"]
        wind["ID"] = index
        wind = pd.DataFrame.from_dict([wind])

        # visibility
        visibility = {}
        visibility["visibility"] = forecast_3hr["visibility"]
        visibility["ID"] = index
        visibility = pd.DataFrame.from_dict([visibility])

        # rain
        rain = {}
        if "rain" not in weather:
          rain["rain"] = 0
        else:
          rain["rain"] = visibility = forecast_3hr["rain"]["3h"]
        rain["ID"] = index
        rain = pd.DataFrame.from_dict([rain])

        # joins the dataframes into a single row of data
        forecast_row = pd.merge(location, time, left_on='ID', right_on='ID', sort=False)
        forecast_row = pd.merge(forecast_row, main, left_on='ID', right_on='ID', sort=False)
        forecast_row = pd.merge(forecast_row, weather, left_on='ID', right_on='ID', sort=False)
        forecast_row = pd.merge(forecast_row, wind, left_on='ID', right_on='ID', sort=False)
        forecast_row = pd.merge(forecast_row, visibility, left_on='ID', right_on='ID', sort=False)
        forecast_row = pd.merge(forecast_row, rain, left_on='ID', right_on='ID', sort=False)

        # append data as we iterate through each city
        append_rows(forecast_row)

    nonlocal forecast_df
    return forecast_df


  def append_rows(forecast_row):
    nonlocal forecast_df
    # append data to forecast_df as we iterate through each city
    forecast_df = pd.concat([forecast_df, forecast_row], ignore_index=True)


  def output_table(processed_data):
    processed_data.set_index('ID', drop=True, inplace=True)
    # generates a dictionary where each key contains a list of values as required by Tableau
    processed_data = processed_data.to_dict('list')
    return processed_data


  # return statement for forecast_weather()
  return get_data(cities, api_key)


# protects the entry point of the script used during local development
if __name__ == '__main__':
  api_key = env_dict["API_KEY"]
  # reads the .csv files containing a list of cities
  cities_df = pd.read_csv('cities.csv', header=[0])
  # converts the dataframe to a dict with records orient
  cities = cities_df.to_dict('records')
  # used to time performance of the script
  t1 = time.perf_counter()
  # print the resulting dataset as a dataframe for readability
  print(pd.DataFrame(forecast_weather(cities, api_key)))
  t2 = time.perf_counter()
  print(f'Finished in {t2-t1} seconds')
else:
  """
  uncomment the following assignments and return statement to run this script as a Tabpy function.
  """
  #api_key = "API_KEY"
  # #creates a dataframe of cities from the input table (.csv file)
  #cities_df = pd.DataFrame(_arg1)
  # #converts the dataframe to a dict with records orient
  #cities = cities_df.to_dict('records')
  #return forecast_weather(cities)
