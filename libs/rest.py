import requests

# gets current weather data for the specified geolocation
def current_weather(api_key):
  url = f'https://api.openweathermap.org/data/2.5/weather?lat=30.2711286&lon=-97.7436995&appid={api_key}'

  response = requests.request("GET", url)

  payload = response.json()

  return payload

# gets 5 day weather forecast data for the specified geolocation
def forecast(api_key):
  url = f'https://api.openweathermap.org/data/2.5/forecast?lat=30.2711286&lon=-97.7436995&appid={api_key}'

  response = requests.request("GET", url)

  payload = response.json()

  return payload
