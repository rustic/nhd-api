import json
import os
import pathlib
import time
from os.path import dirname, join

import requests
from dotenv import load_dotenv

# Create .env file path.
dotenv_path = join(dirname(__file__), '.env')
 
# Load file from the path.
# The .env file containes 3 entries for authentication: CLIENT_ID CLIENT_SECRET NHDSERVER
load_dotenv(dotenv_path)

# Function to see if API Token exists and is less than an hour old.
# Fetches the existing token or requests a new one and stores it to a file
def checkAPIKey():
    apifile = "file.api"
    path = pathlib.Path(apifile)
    if path.exists() and path.is_file:
        st = os.stat(apifile)
        if (time.time() - st.st_ctime) < 3600:
            f = open(apifile)
            token = f.read()
            f.close()
            return token
        else:
            os.unlink(apifile)
            f = open(apifile, 'w')
            token = getAPIKey()
            f.write(token)
            f.close()
            return token
    else:
        f = open(apifile, 'w')
        f.write(getAPIKey())
        f.close()
        return checkAPIKey()

# Function to request an authentication token
def getAPIKey():
    client_id = os.getenv('CLIENT_ID')
    client_secret = os.getenv('CLIENT_SECRET')
    grant_type = 'client_credentials'
    nhdserver = os.getenv('NHDSERVER')
    media = {'Content-Type': 'application/x-www-form-urlencoded'}
    payload = {'grant_type': grant_type, 'client_id': client_id, 'client_secret': client_secret}
    loginapi = 'auth/token'

    apikey = requests.post('https://' + nhdserver + '/' + loginapi, data=payload, headers=media)

    x = json.loads(apikey.text)
    return x['access_token']

# Make the API Request
def ticketQuery(method, uri):
    nhdserver = os.getenv('NHDSERVER')
    token = "Bearer " + checkAPIKey()
    payload = {"Authorization": token}
    url = 'https://' + nhdserver + '/api/' + uri
    tix = requests.request(method, url, headers=payload)
    print(url) # Output the URL queried
    print(tix) # Output the Status code
    print(tix.text) # Output the JSON Text of the query

# Query syntax as per https://www.nethelpdesk.com/apidoc#/resources/tickets?_k=91dis1
ticketQuery("GET", "Tickets") # 404 File not found error
ticketQuery("GET", "Tickets/1004451") # Works
