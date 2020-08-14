#!/usr/bin/env python
# -*- coding: utf-8 -*-

from brewerydb import *
import os
from dotenv import load_dotenv
import json

load_dotenv()

apikey = os.getenv('SECRET_KEY')
baseuri = DEFAULT_BASE_URI

# test apikey imported successfully from .env file, comment this out before pushing to git!!!
# print(apikey)

# configure api key use for session at hand
BreweryDb.configure(apikey, baseuri)

# get data on beers as a dict
beer_data = BreweryDb.beers()

print(beer_data)

beer_data_json = json.dumps(beer_data)

print(beer_data_json)

with open('beer_data.json', 'w') as outfile:
    json.dump(beer_data_json, outfile)
