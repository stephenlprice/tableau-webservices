def current_weather(cities):
  import requests
  import pandas as pd

  api_key = "API Key"

  # creates a data frame from current weather data
  def current(api_key, cities):
    payload = rest_current(api_key, cities)
    data = transform_current(payload, cities)
    return data

  # gets current weather data for the specified geolocation
  def rest_current(api_key, cities):
    url = f'https://api.openweathermap.org/data/2.5/weather?lat=30.2711286&lon=-97.7436995&appid={api_key}&units=imperial'
    response = requests.get(url)
    payload = response.json()
    return payload

  # creates a dataframe from the JSON payload with current weather
  def transform_current(payload, cities):
    # coordinates
    coord = payload["coord"]
    coord["ID"] = 1
    coord = pd.DataFrame.from_dict([coord])

    # weather results
    weather = payload["weather"][0]
    del weather["id"]
    weather["ID"] = 1
    weather = pd.DataFrame.from_dict([weather])

    # main weather data
    main = payload["main"]
    main["ID"] = 1
    main = pd.DataFrame.from_dict([main])

    # visibility 
    visibility = {}
    visibility["visibility"] = payload["visibility"]
    visibility["ID"] = 1
    visibility = pd.DataFrame.from_dict([visibility])

    # wind
    wind = {}
    wind["wind speed"] = payload["wind"]["speed"]
    wind["wind deg"] = payload["wind"]["deg"]
    wind["ID"] = 1
    wind = pd.DataFrame.from_dict([wind])

    # clouds
    clouds = {}
    clouds["clouds"] = payload["clouds"]["all"]
    clouds["ID"] = 1
    clouds = pd.DataFrame.from_dict([clouds])

    # country
    country = {}
    country["country"] = payload["sys"]["country"]
    country["ID"] = 1
    country = pd.DataFrame.from_dict([country])

    # name (city)
    name = {}
    name["name"] = payload["name"]
    name["ID"] = 1
    name = pd.DataFrame.from_dict([name])

    # joins the dataframes into a single row of data
    data = pd.merge(coord, weather, left_on='ID', right_on='ID', sort=False)
    data = pd.merge(data, main, left_on='ID', right_on='ID', sort=False)
    data = pd.merge(data, visibility, left_on='ID', right_on='ID', sort=False)
    data = pd.merge(data, wind, left_on='ID', right_on='ID', sort=False)
    data = pd.merge(data, clouds, left_on='ID', right_on='ID', sort=False)
    data = pd.merge(data, country, left_on='ID', right_on='ID', sort=False)
    data = pd.merge(data, name, left_on='ID', right_on='ID', sort=False)

    data.set_index("ID", drop=True, inplace=True)
    data = data.to_dict('list')

    return data

  return current(api_key, cities)

cities = {
  "Austin": {
    "lon": -97.7436995,
    "lat": 30.2711286,
  },
  "Dallas": {
    "lon": -96.7969,
    "lat": 32.7763
  },
  "Houston": {
    "lon": -95.3677,
    "lat": 29.7589
  },
  "San Antonio": {
    "lon": -98.4936,
    "lat": 29.4241
  },
  "Denver": {
    "lon": -104.9847,
    "lat": 39.7392
  },
  "New Orleans": {
    "lon": -90.0701,
    "lat": 29.9499
  },
  "Tulsa": {
    "lon": -95.9929,
    "lat": 36.1557
  },
  "Oklahoma City": {
    "lon": -97.5171,
    "lat": 35.473
  },
  "Santa Fe": {
    "lon": -105.9506,
    "lat": 35.5167
  },
  "Albuquerque": {
    "lon": -106.6511,
    "lat": 35.0845
  },
  "Monterrey": {
    "lon": -100.3167,
    "lat": 25.6667
  },
  "Mexico City": {
    "lon": -99.1277,
    "lat": 19.4285
  },
  "Havana": {
    "lon": -82.383,
    "lat": 23.133
  }
}

# runs the script
print(current_weather(cities))
