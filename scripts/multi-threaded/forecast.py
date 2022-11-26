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
import concurrent.futures
import requests

# gets weather data for the specified geolocations
def get_data(cities, api_key):
  # a dict to store weather forecast data for each city
  forecasts = {}
  # session object for HTTP persistent connections (https://requests.readthedocs.io/en/latest/user/advanced/#session-objects)
  session = requests.Session()
  # sends a request per city
  def request_data(city, api_key):
    lon = city["lon"]
    lat = city["lat"]
    query_parameters = f'lat={lat}&lon={lon}&appid={api_key}&units=imperial'
    url = f'https://api.openweathermap.org/data/2.5/forecast?{query_parameters}'
    
    nonlocal session
    req = session.get(url)
    # response is serialized into json
    payload = req.json()
    # payload contains 8, 3hr forecast for 5 days (40 individual forecasts per city)
    return payload
  
  # use a pool of threads to execute async calls (https://docs.python.org/3/library/concurrent.futures.html#concurrent.futures.ThreadPoolExecutor)
  with concurrent.futures.ThreadPoolExecutor() as executor:
    # list comprehension loops through every city to request API data with thread pools
    results = [executor.submit(request_data, city, api_key) for city in cities]
  try:
    # catching the returned future (non-blocking threads)
    for future in concurrent.futures.as_completed(results):
      result = future.result()
      # add the json response as a value for each city name key
      name = result["city"]["name"]
      forecasts[name] = result
  except Exception as exc:
    print(f'Thread failed at: {exc}')
  else:
    # returns the dict with city name as key and json payload with 40 forecasts as value   
    return forecasts


# creates dataframes from each 3hr forecast and appends them to a single dataframe
def process(forecasts):
  forecast_df = pd.DataFrame()
  # append data to a dataframe as the process() iterates through each city
  def append_rows(forecast_row):
    nonlocal forecast_df
    # append data to forecast_df as we iterate through each city
    forecast_df = pd.concat([forecast_df, forecast_row], ignore_index=True)

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
      
      # appends each row to a single dataframe (forecast_df)
      append_rows(forecast_row)

  return forecast_df


# output a dict of lists as required by Tableau
def make_table(processed_data):
  processed_data.set_index('ID', drop=True, inplace=True)
  # generates a dictionary where each key contains a list of values
  processed_data = processed_data.to_dict('list')
  return processed_data

# protects the entry point of the script so that this only runs during local development
if __name__ == '__main__':
  api_key = env_dict["API_KEY"]
  # decorator used to run script operations and measure performance
  def run_perf(func, *args, **kwargs):
    # start measuring operation performance
    start = time.perf_counter()
    # obtain the operation string used to print the message and remove it from kwargs
    operation = kwargs["operation"]
    del kwargs["operation"]
    # run the provided function
    result = func(*args, **kwargs)
    # stop measuring operation performance
    finish = time.perf_counter()
    # calculate operation performance
    performance = finish - start
    print(f'{operation} finished in {performance} second(s)')
    return {"result": result, "performance": performance}

  # time module measures performance of each operation and the entire script
  script_start = time.perf_counter()
  
  # reads the .csv files containing a list of cities
  cities_dict = run_perf(pd.read_csv, 'cities2.csv', header=[0], operation='File read')
  cities = cities_dict["result"].to_dict('records')

  # request data from OpenWeather API
  forecasts_dict = run_perf(get_data, cities, api_key, operation='REST API calls')

  # create a single dataframe containing all forecasts
  processed_dict = run_perf(process, forecasts_dict["result"], operation='Data processing')

  # formats the dataframe into a dict for Tableau
  output_dict = run_perf(make_table, processed_dict["result"], operation='Output table')
  # formats the Tableau dict into a dataframe to print results to the console
  output = pd.DataFrame(output_dict["result"])

  # print the resulting dataset as a dataframe for readability
  print("""
    -------------------------------------------------------------------------------------
    **************                    WEATHER FORECASTS                    **************
  """)
  print(output)

  # calculate script and individual operation performance
  script_finish = time.perf_counter()
  t_script = script_finish - script_start
  read_ratio = f'Read:{cities_dict["performance"]/t_script:.2%} ({cities_dict["performance"]:.2f}s)'
  rest_ratio = f'Rest:{forecasts_dict["performance"]/t_script:.2%} ({forecasts_dict["performance"]:.2f}s)'
  process_ratio = f'Process:{processed_dict["performance"]/t_script:.2%} ({processed_dict["performance"]:.2f}s)'
  table_ratio = f'Table Output:{output_dict["performance"]/t_script:.2%} ({output_dict["performance"]:.2f}s)'
  print(f'Script finished in {t_script} second(s)')
  print(f'Composition --> [ {read_ratio} | {rest_ratio} | {process_ratio} | {table_ratio} ]')
else:
  """
  uncomment the following assignments and return statement to run this script as a Tabpy function.
  """
  # api_key = "API_KEY"
  # # creates a dataframe of cities from the input table (.csv file)
  # cities_df = pd.DataFrame(_arg1)
  # # converts the dataframe to a dict with records orient
  # cities = cities_df.to_dict('records')
  # # request data from OpenWeather API
  # forecasts = get_data(cities, api_key)
  # # create a single dataframe containing all forecasts
  # processed_data = process(forecasts)
  # # formats the dataframe into a dict for Tableau
  # output_dict = make_table(processed_data)
  # # return statement for the Table Extensions Function
  # return output_dict
