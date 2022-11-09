import os
from dotenv import load_dotenv
from modules import data

# load environment files from .env
load_dotenv(".env")
# calling environ is expensive, this saves environment variables to a dictionary
env_dict = dict(os.environ)

api_key = env_dict["API_KEY"]

df = data.forecast(api_key)

print(df)
