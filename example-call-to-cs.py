#!/usr/bin/env python
# -*- coding: utf-8 -*-

# import packages/modules
from google.cloud import storage
from google.cloud import secretmanager
from localpackage.brewerydb import *
import json

# setup scret manager, pull secret key for api wrapper
# PREREQUISITE: must give GCP service account the 'Secret Manager Secret Accessor' role !!!
client = secretmanager.SecretManagerServiceClient()
secret_name = "secret-api-key"
project_id = "project-id"
resource_name = f"projects/{project_id}/secrets/{secret_name}/versions/latest"
response = client.access_secret_version(resource_name)
secret_string = response.payload.data.decode('UTF-8')

# api wrapper variables
apikey = secret_string
baseuri = DEFAULT_BASE_URI


# define main function in cloud function, in this case...
# ...make API call using an API wrapper package...
# ...get dict response, convert to JSON, write to tmp directory...
# ...upload file to storage bucket
def main(request):

    # configure api key use for session at hand
    BreweryDb.configure(apikey, baseuri)

    # get data on beers as a dict - returns one of many pages...
    # ...TODO create a loop for calling all pages and appending
    beer_data = BreweryDb.beers()

    # prints the response dict (with single quotes)
    print(beer_data)

    # convert returned dict to json
    beer_data_json = json.dumps(beer_data)

    # prints the json type (with double quotes)
    print(beer_data_json)

    # provide path and filename to with open as outfile:
    with open('/tmp/' + 'beer_data_json.json', 'w') as outfile:
        json.dump(beer_data_json, outfile)

    # function for uploading to cloud storage
    def upload_blob(file_name):
        bucket_name = 'bucket-name'
        storage_client = storage.Client("project-id")
        bucket = storage_client.get_bucket(bucket_name)
        blob = bucket.blob(file_name)
        blob.upload_from_filename(file_name)

        print('BEGINNING EXPORT.')

    # call function for upload
    upload_blob('filename')
