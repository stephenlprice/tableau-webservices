import pandas as pd
import json
from libs import rest, transform

# creates a data frame from forecast data
def current(api_key):
  payload = rest.current(api_key)
  data = transform.current(payload)

  return data


# creates a data frame from forecast data
def forecast(api_key):
  payload = rest.forecast(api_key)
  data = transform.forecast(payload)
  
  return data
