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
import traceback
import concurrent.futures
import requests
import pandas as pd

# gets weather data for the specified geolocations
def get_data(cities, api_key):
  # a dict of current weather data per city
  weather_data = {}
  # session object for HTTP persistent connections (https://requests.readthedocs.io/en/latest/user/advanced/#session-objects)
  session = requests.Session()
  # sends a request per city
  def request_data(city, api_key):
    lon = city["lon"]
    lat = city["lat"]
    query_parameters = f'lat={lat}&lon={lon}&appid={api_key}&units=imperial'
    url = f'https://api.openweathermap.org/data/2.5/weather?{query_parameters}'
    
    nonlocal session
    req = session.get(url)
    # response is serialized into json
    payload = req.json()
    # payload contains current weather for each city
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
      name = result["name"]
      weather_data[name] = result
  except:
    print(f'ERROR: Thread failed at:')
    traceback.print_exc()
  else:
    # returns the dict with city name as key and json payload as value   
    return weather_data


# creates dataframes from each city and appends them to a single dataframe
def process(cities):
  weather_df = pd.DataFrame()
  # append data to a dataframe as the process() iterates through each city
  def append_rows(city_row):
    nonlocal weather_df
    # append data to weather_df as we iterate through each city
    weather_df = pd.concat([weather_df, city_row], ignore_index=True)

  # each row will have a unique index
  index = 0
  for city in cities:
    index = index + 1
    # coordinates
    coord = cities[city]["coord"]
    coord["ID"] = index
    coord = pd.DataFrame.from_dict([coord])

    # weather results
    weather = cities[city]["weather"][0]
    del weather["id"]
    weather["ID"] = index
    weather = pd.DataFrame.from_dict([weather])

    # main weather data
    main = cities[city]["main"]
    if "sea_level" in main:
      del main["sea_level"]
    if "grnd_level" in main:
      del main["grnd_level"]
    main["ID"] = index
    main = pd.DataFrame.from_dict([main])

    # visibility 
    visibility = {}
    visibility["visibility"] = cities[city]["visibility"]
    visibility["ID"] = index
    visibility = pd.DataFrame.from_dict([visibility])

    # wind
    wind = {}
    wind["wind speed"] = cities[city]["wind"]["speed"]
    wind["wind deg"] = cities[city]["wind"]["deg"]
    wind["ID"] = index
    wind = pd.DataFrame.from_dict([wind])

    # clouds
    clouds = {}
    clouds["clouds"] = cities[city]["clouds"]["all"]
    clouds["ID"] = index
    clouds = pd.DataFrame.from_dict([clouds])

    # country
    country = {}
    country["country"] = cities[city]["sys"]["country"]
    country["ID"] = index
    country = pd.DataFrame.from_dict([country])

    # name (city)
    name = {}
    name["name"] = cities[city]["name"]
    name["city_id"]= cities[city]["id"]
    name["ID"] = index
    name = pd.DataFrame.from_dict([name])

    # joins the dataframes into a single row of data
    city_row = pd.merge(coord, weather, left_on='ID', right_on='ID', sort=False)
    city_row = pd.merge(city_row, main, left_on='ID', right_on='ID', sort=False)
    city_row = pd.merge(city_row, visibility, left_on='ID', right_on='ID', sort=False)
    city_row = pd.merge(city_row, wind, left_on='ID', right_on='ID', sort=False)
    city_row = pd.merge(city_row, clouds, left_on='ID', right_on='ID', sort=False)
    city_row = pd.merge(city_row, country, left_on='ID', right_on='ID', sort=False)
    city_row = pd.merge(city_row, name, left_on='ID', right_on='ID', sort=False)
    
    # appends each row to a single dataframe (forecast_df)
    append_rows(city_row)

  return weather_df


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
  cities_dict = run_perf(pd.read_csv, 'data/cities_40.csv', header=[0], operation='File read')
  cities = cities_dict["result"].to_dict('records')

  # request data from OpenWeather API
  current_dict = run_perf(get_data, cities, api_key, operation='REST API calls')

  # create a single dataframe containing all city data
  processed_dict = run_perf(process, current_dict["result"], operation='Data processing')

  # formats the dataframe into a dict for Tableau
  output_dict = run_perf(make_table, processed_dict["result"], operation='Output table')
  output = pd.DataFrame(output_dict["result"])

  # print the resulting dataset as a dataframe for readability
  print("""
    -------------------------------------------------------------------------------------
    **************                     CURRENT WEATHER                     **************
  """)
  print(output)

  # calculate script and individual operation performance
  script_finish = time.perf_counter()
  t_script = script_finish - script_start
  read_ratio = f'Read:{cities_dict["performance"]/t_script:.2%} ({cities_dict["performance"]:.2f}s)'
  rest_ratio = f'Rest:{current_dict["performance"]/t_script:.2%} ({current_dict["performance"]:.2f}s)'
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
  # # create a single dataframe containing all city data
  # processed_data = process(forecasts)
  # # formats the dataframe into a dict for Tableau
  # output_dict = make_table(processed_data)
  # # return statement for the Table Extensions Function
  # return output_dict
