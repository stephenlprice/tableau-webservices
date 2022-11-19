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
  def get_data(api_key, cities):
    # a dict of weather forecast data per city
    city_forecast = {}
    index = 0
    # session object with python 3.2's concurrent.futures allowing for async requests
    session = FuturesSession(executor=ThreadPoolExecutor(max_workers=8))

    request_cnt = 0
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
      city_forecast[name] = payload

      request_cnt = request_cnt + 1
      print(f'request_cnt: {request_cnt}')

    # created a thread pool for parralel processing
    with ThreadPoolExecutor(max_workers=12) as executor:  
      print(f'city_forecast: {city_forecast}')
      # submit the task
      processed_data = executor.submit(process_data, city_forecast, forecast_df, index)
      # get the result and format the dataframe to a dict of lists for Tableau
      forecast_data = output_table(processed_data.result())
 
    return forecast_data
      

  def process_data(city_forecast, forecast_df, index):
    process_cnt = 0
    # create a row of data with each 3 hour forecast
    city_row = create_rows(city_forecast, index)
    # creates a single dataframe with all rows
    processed_data = append_rows(city_row, forecast_df)
    print(f'processed_data: {processed_data}')

    process_cnt = process_cnt + 1
    print(f'process_cnt: {process_cnt}')

    return processed_data


  def create_rows(city_forecast, index):
    city_cnt = 0
    for city in city_forecast:
      # payload per city contains a list with 5 day forecast every 3 hours
      forecasts = city_forecast[city]["list"]
      for forecast in forecasts:
        index = index + 1
        # location
        location = {}
        location["city_id"]= city_forecast[city]["city"]["id"]
        location["name"]= city_forecast[city]["city"]["name"]
        location["country"]= city_forecast[city]["city"]["country"]
        location["lat"]= city_forecast[city]["city"]["coord"]["lat"]
        location["lon"]= city_forecast[city]["city"]["coord"]["lon"]
        location["ID"] = index
        location = pd.DataFrame.from_dict([location])

        # timestamp and unix epoch
        time = {}
        time["timestamp"] = forecast["dt_txt"]
        time["unix_epoch"] = forecast["dt"]
        time["ID"] = index
        time = pd.DataFrame.from_dict([time])

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
        wind = pd.DataFrame.from_dict([wind])

        # visibility
        visibility = {}
        visibility["visibility"] = forecast["visibility"]
        visibility["ID"] = index
        visibility = pd.DataFrame.from_dict([visibility])

        # rain
        rain = {}
        if "rain" not in weather:
          rain["rain"] = 0
        else:
          rain["rain"] = visibility = forecast["rain"]["3h"]
        rain["ID"] = index
        rain = pd.DataFrame.from_dict([rain])

        # joins the dataframes into a single row of data
        city_row = pd.merge(location, time, left_on='ID', right_on='ID', sort=False)
        city_row = pd.merge(city_row, main, left_on='ID', right_on='ID', sort=False)
        city_row = pd.merge(city_row, weather, left_on='ID', right_on='ID', sort=False)
        city_row = pd.merge(city_row, wind, left_on='ID', right_on='ID', sort=False)
        city_row = pd.merge(city_row, visibility, left_on='ID', right_on='ID', sort=False)
        city_row = pd.merge(city_row, rain, left_on='ID', right_on='ID', sort=False)

        city_cnt = city_cnt + 1
        print(f'city_cnt: {city_cnt}')

    return city_row


  def append_rows(city_row, forecast_df):
    # append data to forecast_df as we iterate through each city
    forecast_df = pd.concat([forecast_df, city_row], ignore_index=True)
    print(f'forecast_df: {forecast_df}')
    return forecast_df


  def output_table(forecast_df):
    # generates a dictionary where each key contains a list of values as required by Tableau
    forecast_df.set_index('ID', drop=True, inplace=True)
    forecast_data = forecast_df.to_dict('list')
    return forecast_data

  # return statement for forecast_weather()
  return get_data(api_key, cities)


# protects the entry point of the script used during local development
if __name__ == '__main__':
  api_key = env_dict["API_KEY"]
  # reads the .csv files containing a list of cities
  cities_df = pd.read_csv('cities.csv', header=[0])
  # converts the dataframe to a dict with records orient
  cities = cities_df.to_dict('records')
  # print the resulting dataset as a dataframe for readability
  print(pd.DataFrame(forecast_weather(cities, api_key)))
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
