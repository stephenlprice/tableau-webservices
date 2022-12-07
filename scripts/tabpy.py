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

def create_df(data_type, data):
  weather_df = pd.DataFrame()
  # append data to a dataframe as the process() iterates through each city
  def append_rows(data_row):
    nonlocal weather_df
    # append data to weather_df as we iterate through each city
    weather_df = pd.concat([weather_df, data_row], ignore_index=True)

  # creates a row from current weather data
  def current_weather(data):
    # each row will have a unique index
    index = data["id"]
    # coordinates
    coord = data["coord"]
    coord["ID"] = index
    coord = pd.DataFrame.from_dict([coord])

    # weather results
    weather = data["weather"][0]
    del weather["id"]
    weather["ID"] = index
    weather = pd.DataFrame.from_dict([weather])

    # main weather data
    main = data["main"]
    if "sea_level" in main:
      del main["sea_level"]
    if "grnd_level" in main:
      del main["grnd_level"]
    main["ID"] = index
    main = pd.DataFrame.from_dict([main])

    # visibility 
    visibility = {}
    visibility["visibility"] = data["visibility"]
    visibility["ID"] = index
    visibility = pd.DataFrame.from_dict([visibility])

    # wind
    wind = {}
    wind["wind speed"] = data["wind"]["speed"]
    wind["wind deg"] = data["wind"]["deg"]
    wind["ID"] = index
    wind = pd.DataFrame.from_dict([wind])

    # clouds
    clouds = {}
    clouds["clouds"] = data["clouds"]["all"]
    clouds["ID"] = index
    clouds = pd.DataFrame.from_dict([clouds])

    # country
    country = {}
    country["country"] = data["sys"]["country"]
    country["ID"] = index
    country = pd.DataFrame.from_dict([country])

    # name (city)
    name = {}
    name["name"] = data["name"]
    name["city_id"]= data["id"]
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
  def weather_forecast(data):
    # each row will have a unique index
    index = 0
    for forecast in data:
      forecast_list = data[forecast]["list"]
      for forecast_3hr in forecast_list:
        index = index + 1
        # location
        location = {}
        location["city_id"]= data[forecast]["city"]["id"]
        location["name"]= data[forecast]["city"]["name"]
        location["country"]= data[forecast]["city"]["country"]
        location["lat"]= data[forecast]["city"]["coord"]["lat"]
        location["lon"]= data[forecast]["city"]["coord"]["lon"]
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

  if data_type == 'current':
    # dict comprehension creates rows for each city
    {current_weather(data[city]) for city in data}
  elif data_type == 'forecast':
    # dict comprehension creates rows for each city
    {weather_forecast(data[forecast]) for forecast in data}
  else:
    raise Exception('ERROR: data_type must be current or forecast')

  return weather_df


# creates dataframes from each city and appends them to a single dataframe
def process(multiprocess, data_type, data):
  processed_df = pd.DataFrame()
  # spawns processes to process data in parallel
  def process_pooler(func, *args, **kwargs):
    nonlocal processed_df
    with concurrent.futures.ProcessPoolExecutor() as executor:
      task = kwargs["task"]
      del kwargs["task"]
      data_type = kwargs["data_type"]
      del kwargs["data_type"]
      # list comprehension loops through every city to create chunks for each process
      results = {executor.submit(func, data_type, {chunk: task[chunk]}, *args, **kwargs) for chunk in task}
      try:
        # results contains a list of futures that needs to be iterated through
        for future in concurrent.futures.as_completed(results):
          processed_data = future.result()
          # append to final_df as we iterate through dataframes generated by each process
          processed_df = pd.concat([processed_df, processed_data], ignore_index=True)
      except:
        print(f'ERROR: Process failed at:')
        traceback.print_exc()
      else:
        return processed_df

  if multiprocess == False:
    # dict comprehension creates rows for each city
    processed_df = pd.concat([processed_df, {create_df(data[city], data_type) for city in data}], ignore_index=True)
  elif multiprocess == True:
    # runs a process pool for the specified function
    process_pooler(create_df, data_type=data_type, task=data)
  else:
    raise Exception('ERROR: multiprocess must be True or False')

  return processed_df

# output a dict of lists as required by Tableau
def make_table(processed_data):
  processed_data.set_index('ID', drop=True, inplace=True)
  # generates a dictionary where each key contains a list of values
  processed_data = processed_data.to_dict('list')
  return processed_data
