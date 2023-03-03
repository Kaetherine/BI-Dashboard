from datetime import datetime
import json
import pandas as pd
import requests
from sqlalchemy import create_engine

positions = [
    # 'SAP-Entwickler/SAP-Berater',
    # 'IT-Projektmanager',
    # 'Softwareentwickler',
    # 'Business Intelligence Analyst',
    # 'IT-Controller',
    # 'IT-Berater',
    # 'Produktmanager',
    # 'App-Entwickler',
    # 'Anwendungsentwickler',
    # 'Datenbankspezialist',
    # 'ERP Manager',
    'Data Analyst',
    # 'Data Scientist',
    # 'Data Engineer',
    # 'Data Visualisation Engineer',
    # 'Projet Manager',
    # 'Product Manager'
]

base_url = "https://rest.arbeitsagentur.de/"
jobboerse = "jobboerse/jobsuche-service/pc/v4/jobs?angebotsart=1&was="
page_nav = "&page=1&size=25&pav=false"
# job = "https://rest.arbeitsagentur.de/jobboerse/jobsuche-service/pc/v2/jobdetails/MTIyODgtMjg5MzEwMDE1OS1T"

joblistings = []

for position in positions:
    joblist_url = f'{base_url}{jobboerse}{position}{page_nav}'
    response = requests.get(joblist_url)
    json_response = json.loads(response.text)
    for listing in json_response['stellenangebote']:
        print(listing, '\n')