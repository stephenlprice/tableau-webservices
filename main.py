# imports used for local development
import os, time
from dotenv import load_dotenv
import pandas as pd
from scripts import tabpy

# load environment files from .env
load_dotenv(".env")
# calling environ is expensive, this saves environment variables to a dictionary
env_dict = dict(os.environ)
api_key = env_dict["API_KEY"]

# stores performance recording to output at script end
perf_dict = {}
# decorator used to run script operations and measure performance
def run_perf(func, *args, **kwargs):
  # obtain the operation string used to print the message and remove it from kwargs
  operation = kwargs["operation"]
  del kwargs["operation"]
  # start measuring operation performance
  start = time.perf_counter()
  # run the provided function
  result = func(*args, **kwargs)
  # stop measuring operation performance
  finish = time.perf_counter()
  # calculate operation performance
  performance = finish - start
  # add performance recording to perf_dict
  perf_dict[operation] = performance
  print(f'{operation} finished in {performance} second(s)')
  return result
  

# prints performance recordings to compare techniques
def print_perf(perf_dict, t_script):
  # dict comprehension to store message strings for each operation
  ratios = {f'{operation}': f'{operation}:{perf_dict[operation]/t_script:.2%} ({perf_dict[operation]:.2f}s)' for operation in perf_dict}
  message = 'Composition --> ['
  for ratio in ratios:
    message += f' {ratios[ratio]} |'
  message = message[:-1] + ']'
  print("""
    -------------------------------------------------------------------------------------
    **************                       PERFORMANCE                       **************
  """)
  print(f'Script finished in {t_script} second(s)')
  # prints the percentage that operation contributed to total script runtime
  print(message)

# protects the entry point of the script so that this only runs during local development
if __name__ == '__main__':
  # measures performance of each operation and the entire script
  script_start = time.perf_counter()
  # reads the .csv files containing a list of cities
  cities_dict = run_perf(pd.read_csv, 'data/cities_40.csv', header=[0], operation='File read')
  cities = cities_dict.to_dict('records')
  # request data from OpenWeather API
  weather_dict = run_perf(tabpy.get_data, cities, api_key, operation='REST API calls')
  # starts a process pooler to run processing in parallel
  processed_df = run_perf(tabpy.process, False, "current", weather_dict, operation='Process pool')
  # print the resulting dataset as a dataframe for readability
  print("""
    -------------------------------------------------------------------------------------
    **************                     CURRENT WEATHER                     **************
  """)
  print(processed_df)
  # calculate script and individual operation performance
  script_finish = time.perf_counter()
  t_script = script_finish - script_start
  # print performance results
  print_perf(perf_dict, t_script)
  