import pandas as pd

# creates a dataframe from the JSON payload with current weather
def current(payload):
  keys = payload.keys()

  # print(type(payload))
  # print(keys)
  # print(json.dumps(payload, indent=3))

  # coordinates
  coord = payload["coord"]
  coord["row"] = 1
  coord = pd.DataFrame.from_dict([coord])

  # weather results
  weather = payload["weather"][0]
  del weather["id"]
  weather["row"] = 1
  weather = pd.DataFrame.from_dict([weather])

  # main weather data
  main = payload["main"]
  main["row"] = 1
  main = pd.DataFrame.from_dict([main])


  # visibility 
  visibility = {}
  visibility["visibility"] = payload["visibility"]
  visibility["row"] = 1
  visibility = pd.DataFrame.from_dict([visibility])


  # wind
  wind = {}
  wind["wind speed"] = payload["wind"]["speed"]
  wind["wind deg"] = payload["wind"]["deg"]
  wind["row"] = 1
  wind = pd.DataFrame.from_dict([wind])


  # clouds
  clouds = {}
  clouds["clouds"] = payload["clouds"]["all"]
  clouds["row"] = 1
  clouds = pd.DataFrame.from_dict([clouds])


  # country
  country = {}
  country["country"] = payload["sys"]["country"]
  country["row"] = 1
  country = pd.DataFrame.from_dict([country])


  # name (city)
  name = {}
  name["name"] = payload["name"]
  name["row"] = 1
  name = pd.DataFrame.from_dict([name])

  data = pd.merge(coord, weather, left_on='row', right_on='row', sort=False)
  data = pd.merge(data, main, left_on='row', right_on='row', sort=False)
  data = pd.merge(data, visibility, left_on='row', right_on='row', sort=False)
  data = pd.merge(data, wind, left_on='row', right_on='row', sort=False)
  data = pd.merge(data, clouds, left_on='row', right_on='row', sort=False)
  data = pd.merge(data, country, left_on='row', right_on='row', sort=False)
  data = pd.merge(data, name, left_on='row', right_on='row', sort=False)

  return data


def forecast(payload):

  print(type(payload))
  print(payload)
  