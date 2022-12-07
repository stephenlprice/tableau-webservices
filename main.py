"""
-------------------------------------------------------------------------------------
*******           TABLEAU WEB SERVICES (OPENWEATHER API)           *******

Request current weather data from the OpenWeather API via Table Extensions.

Table Extension scripts are essentially functions with a return statement. 
However, in order to support local development the script is run from main.py 
so that performance recording and load testing can be done separate from 
Tabpy code. Therefore when running main.py, the script can output results to 
a shell without resulting in: (`SyntaxError: 'return' outside function`).

This file is not meant to be sent to Tabpy and is only intended for local 
development. The main.py file is the equivalent of protecting the Tabpy 
script with `(__name__ == '__main__')` to avoid sending this unuseable code 
to Tabpy while keeping the code separate and more organized.

To secure the necessary API key, use a .env file (see README.md) during local
development. This avoids pushing your key to public repositories such as Github.
When deployed to a Table Extension you can hardcode the API key in the script.
-------------------------------------------------------------------------------------
"""
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

class OpenWeather_Job:
  def __init__(self, multithreading, multiprocessing, input_data, api_key):
    # True or False
    self.multithreading = multithreading
    # True or False
    self.multiprocessing = multiprocessing
    # .csv file
    self.input_data = input_data
    # key for OpenWeather API
    self.api_key = api_key
    # stores performance recording to output at script end
    self.perf_dict = {}
    # 
    self.script_perf = 0

  def __str__(self):
    return f"OpenWeather_Job: multithreading: {self.multithreading}, multiprocessing: {self.multiprocessing}"

  # private decorator used to run script operations and measure performance
  def __run_perf(self, func, *args, **kwargs):
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
    self.perf_dict[operation] = performance
    print(f'{operation} finished in {performance} second(s)')
    return result

  # prints performance recordings to compare techniques
  def print_perf(self):
    perf_dict = self.perf_dict
    script_perf = self.script_perf
    # dict comprehension to store message strings for each operation
    ratios = {f'{operation}': f'{operation}:{perf_dict[operation]/script_perf:.2%} ({perf_dict[operation]:.2f}s)' for operation in perf_dict}
    message = 'Composition --> ['
    for ratio in ratios:
      message += f' {ratios[ratio]} |'
    message = message[:-1] + ']\n'
    print(f'      //////////////    Multi-threading: {self.multithreading} | Multi-processing: {self.multiprocessing}    ///////////////\n')
    print(f'Script finished in {script_perf} second(s)')
    # prints the percentage that operation contributed to total script runtime
    print(message)

  def run_job(self):
    # measures performance of each operation and the entire script
    script_start = time.perf_counter()
    # reads the .csv files containing a list of cities
    cities_dict = self.__run_perf(pd.read_csv, self.input_data, header=[0], operation='File read')
    cities = cities_dict.to_dict('records')
    # request data from OpenWeather API
    weather_dict = self.__run_perf(tabpy.get_data, cities, api_key, self.multithreading, operation='REST API calls')
    # starts a process pooler to run processing in parallel
    processed_df = self.__run_perf(tabpy.process, self.multiprocessing, "current", weather_dict, operation='Process pool')
    # print the resulting dataset as a dataframe for readability
    print("""
      -------------------------------------------------------------------------------------
      **************                     CURRENT WEATHER                     **************
    """)
    print(f'      //////////////    Multi-threading: {self.multithreading} | Multi-processing: {self.multiprocessing}    ///////////////\n')
    print(processed_df, '\n')
    # calculate script and individual operation performance
    script_finish = time.perf_counter()
    self.script_perf = script_finish - script_start

      
# protects the entry point of the script so that this only runs during local development
if __name__ == '__main__':
  input_data = 'data/cities_5.csv'
  

  # Object constructor: OpenWeather_Job(multithreading, multiprocessing, input_data, api_key)
  singleThread_singleProcess = OpenWeather_Job(False, False, input_data, api_key)
  singleThread_singleProcess.run_job()

  multiThread_singleProcess = OpenWeather_Job(True, False, input_data, api_key)
  multiThread_singleProcess.run_job()

  multiThread_multiProcess = OpenWeather_Job(True, True, input_data, api_key)
  multiThread_multiProcess.run_job()

  print("""
      -------------------------------------------------------------------------------------
      **************                       PERFORMANCE                       **************
    """)
  singleThread_singleProcess.print_perf()
  multiThread_singleProcess.print_perf()
  multiThread_multiProcess.print_perf()