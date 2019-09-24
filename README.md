# NetHelpDesk AP Testing
### This repo contains scripts that are useful in testing the NetHelpdesk API

**Usage:**

1. Clone the repo:

`git clone https://github.com/rustic/nhd-api.git`

2. Create and access virtual environment

`cd nhd-api && python3 -m venv venv`

`source venv/bin/activate`

`pip install -r requirements.txt`

3. Edit the the `env.sample` file with your client credentials and NHD server

4. Save the file as `.env`

Test out the API with `python nhd-apitest.py`