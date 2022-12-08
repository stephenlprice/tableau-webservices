"""
----------------------------------------------------------------------------
********           TABLEAU WEB SERVICES (OPENWEATHER API)           ********

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
-------------------------------------------------------------------------------
"""
# imports used for local development
import os, time
from dotenv import load_dotenv
import pandas as pd
import tabpy

class OpenWeather_Job:
  """
    This class defines inputs and functions that can run "jobs" or requests for data from 
    the OpenWeather API to obtain current weather and 5 day 3 hour forecasts for each city 
    listed on an input table. "Jobs" run different function configurations to simulate 
    running Tabpy scripts under different conditions. These simulations represent how single 
    threaded, multithreaded and multiprocess configuration affect the Tabpy script's ability 
    to deliver a dataset to Tableau under different workloads (number of cities). This class 
    also defines a private function that records performance for analysis.
  """
  def __init__(self, multithreading, multiprocessing, data_type, input_data, api_key):
    # True or False
    self.multithreading = multithreading
    # True or False
    self.multiprocessing = multiprocessing
    # whether the job is a forecast or current weather job
    self.data_type = data_type
    # .csv file
    self.input_data = input_data
    # key for OpenWeather API
    self.api_key = api_key
    # stores performance for all operations
    self.perf_dict = {}
    # stores performance for the entire script
    self.script_perf = 0

    self.__validate()

  def __str__(self):
    return f"OpenWeather_Job: multithreading: {self.multithreading}, multiprocessing: {self.multiprocessing}"

  # private function validates class inputs
  def __validate(self):
    if self.multithreading is not True and self.multithreading is not False:
      raise Exception('multithreading parameter must be True or False')
    if self.multiprocessing is not True and self.multiprocessing is not False:
      raise Exception('multiprocessing parameter must be True or False')
    if self.data_type != "weather" and self.data_type != "forecast":
      raise Exception('data_type parameter must be "weather" or "forecast"')
    
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
    # compose a message string to print performance analysis for each operation
    message = 'Composition --> ['
    for ratio in ratios:
      message += f' {ratios[ratio]} |'
    message = message[:-1] + ']\n'
    print(f'Multi-threading: {self.multithreading} | Multi-processing: {self.multiprocessing}')
    print(f'Script finished in {script_perf} second(s)')
    # prints the percentage that operation contributed to total script runtime
    print(message)
    print(f'      ______________________________________________________________________________________________________________________\n')

  # runs a job as configured by constructor parameters
  def run_job(self):
    # measures performance of each operation and the entire script
    script_start = time.perf_counter()
    # reads the .csv files containing a list of cities
    cities_dict = self.__run_perf(pd.read_csv, self.input_data, header=[0], operation='File read')
    cities = cities_dict.to_dict('records')
    # request data from OpenWeather API
    weather_dict = self.__run_perf(tabpy.get_data, cities, api_key, self.multithreading, self.data_type, operation='REST API calls')
    # starts a process pooler to run processing in parallel
    processed_df = self.__run_perf(tabpy.process, self.multiprocessing, self.data_type, weather_dict, operation='Process pool')
    # print the resulting dataset as a dataframe for readability
    print(f'\nMulti-threading: {self.multithreading} | Multi-processing: {self.multiprocessing}\n')
    print(processed_df)
    print(f'\n      _____________________________________________________________________________________________________________________\n')
    # calculate script and individual operation performance
    script_finish = time.perf_counter()
    # calculate and store overall script performance
    self.script_perf = script_finish - script_start

# protects the entry point of the script so that this only runs during local development
if __name__ == '__main__':
  # load environment files from .env
  load_dotenv(".env")
  # calling environ is expensive, this saves environment variables to a dictionary
  env_dict = dict(os.environ)
  api_key = env_dict["API_KEY"]
  # define global simulation variables (input file, "weather" or "forecast")
  input_data = 'data/cities_5.csv'
  data_type = 'forecast'
  
  # create different job configurations for the simulation
  singleThread_singleProcess = OpenWeather_Job(False, False, data_type,  input_data, api_key)
  multiThread_singleProcess = OpenWeather_Job(True, False, data_type, input_data, api_key)
  multiThread_multiProcess = OpenWeather_Job(True, True, data_type, input_data, api_key)
  
  # run each job and output the resulting table
  print("""
    ------------------------------------------------------------------------------------------------------------------------
    ********************************                       WEATHER DATA                     ********************************
  """)
  singleThread_singleProcess.run_job()
  multiThread_singleProcess.run_job()
  multiThread_multiProcess.run_job()

  # output performance results for each job configuration
  print("""
      ----------------------------------------------------------------------------------------------------------------------
      *******************************                       PERFORMANCE                      *******************************
    """)
  singleThread_singleProcess.print_perf()
  multiThread_singleProcess.print_perf()
  multiThread_multiProcess.print_perf()
