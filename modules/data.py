import pandas
from libs import rest

# creates a data frame from forecast data
def forecast(api_key):
  data = rest.forecast(api_key)
  
  print(data)
