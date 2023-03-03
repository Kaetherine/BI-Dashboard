from datetime import datetime
import json
import pandas as pd
import requests
from sqlalchemy import create_engine
from base64 import b64encode

positions = [
    'SAP-Entwickler/SAP-Berater',
    'IT-Projektmanager',
    'Softwareentwickler',
    'Business Intelligence Analyst',
    'IT-Controller',
    'IT-Berater',
    'Produktmanager',
    'App-Entwickler',
    'Anwendungsentwickler',
    'Datenbankspezialist',
    'ERP Manager',
    'Data Analyst',
    'Data Scientist',
    'Data Engineer',
    'Data Visualisation Engineer',
    'Projektmanager',
]

base_url = "https://rest.arbeitsagentur.de/"
jobboerse = "jobboerse/jobsuche-service/pc/v4/jobs?angebotsart=1&was="
page_nav = "&page=1&size=25&pav=false"

fertigkeiten_count = 0
joblistings = []
for position in positions:
    joblist_url = f'{base_url}{jobboerse}{position}{page_nav}'
    try:
        response = requests.get(joblist_url)
    except KeyError:
        pass
    json_response = json.loads(response.text)

    i = 0
    for listing in json_response['stellenangebote']:

        joblistings.append(listing)
        refnr = json_response['stellenangebote'][i]['refnr']

        code_bytes = bytes(refnr, 'utf-8')
        encoded_code = b64encode(code_bytes)
        job_id = encoded_code.decode()

        job_url = f"{base_url}jobboerse/jobsuche-service/pc/v2/jobdetails/{job_id}"
        job_response = requests.get(job_url)
        job_json_response = json.loads(job_response.text)
        job_keys = list(job_json_response.keys())

        if 'externeUrl' in job_keys:
            pass
        if 'fertigkeiten' in job_keys:
            # print(refnr, '\n')
            # print(job_keys, '\n')
            # print(job_json_response['fertigkeiten'], '\n')
            fertigkeiten_count += 1
        listing.update({'job_id':job_id})
        joblistings.append(listing)
        i += 1

df_joblistings = pd.DataFrame(joblistings)
print(df_joblistings)
print(fertigkeiten_count)