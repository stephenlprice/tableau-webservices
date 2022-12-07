# gets weather data for the specified geolocations
# imports used by the Tabpy Function
import traceback
import concurrent.futures
import requests
import pandas as pd

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
def process(type, data):
  weather_df = pd.DataFrame()
  
  # append data to a dataframe as the process() iterates through each city
  def append_rows(data_row):
    nonlocal weather_df
    # append data to weather_df as we iterate through each city
    weather_df = pd.concat([weather_df, data_row], ignore_index=True)

  # creates a row from current weather data
  def current_weather(city):
    # each row will have a unique index
    index = city["id"]
    # coordinates
    coord = city["coord"]
    coord["ID"] = index
    coord = pd.DataFrame.from_dict([coord])

    # weather results
    weather = city["weather"][0]
    del weather["id"]
    weather["ID"] = index
    weather = pd.DataFrame.from_dict([weather])

    # main weather data
    main = city["main"]
    if "sea_level" in main:
      del main["sea_level"]
    if "grnd_level" in main:
      del main["grnd_level"]
    main["ID"] = index
    main = pd.DataFrame.from_dict([main])

    # visibility 
    visibility = {}
    visibility["visibility"] = city["visibility"]
    visibility["ID"] = index
    visibility = pd.DataFrame.from_dict([visibility])

    # wind
    wind = {}
    wind["wind speed"] = city["wind"]["speed"]
    wind["wind deg"] = city["wind"]["deg"]
    wind["ID"] = index
    wind = pd.DataFrame.from_dict([wind])

    # clouds
    clouds = {}
    clouds["clouds"] = city["clouds"]["all"]
    clouds["ID"] = index
    clouds = pd.DataFrame.from_dict([clouds])

    # country
    country = {}
    country["country"] = city["sys"]["country"]
    country["ID"] = index
    country = pd.DataFrame.from_dict([country])

    # name (city)
    name = {}
    name["name"] = city["name"]
    name["city_id"]= city["id"]
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
  
  # creates a row from 3 hour 5 day weather forecasts
  def weather_forecast(forecasts):
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

  # determine right operation based on data type
  def create_row(data, type):
    if type == 'current':
      # dict comprehension creates rows for each city
      {current_weather(data[city]) for city in data}
    elif type == 'forecast':
      weather_forecast(data)
    else:
      raise Exception('data type must be current or forecast')
    
  create_row(data, type)

  return weather_df

# output a dict of lists as required by Tableau
def make_table(processed_data):
  processed_data.set_index('ID', drop=True, inplace=True)
  # generates a dictionary where each key contains a list of values
  processed_data = processed_data.to_dict('list')
  return processed_data
