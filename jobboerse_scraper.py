from datetime import datetime
import json
import pandas as pd
import requests
from sqlalchemy import create_engine
from base64 import b64encode

def get_page(url, page = False, size = 100):
    if page:
        url = f'{url}&page={page}&size={size}&pav=false'
    try:
        response = requests.get(url)
    except Exception as e:
        raise(e)
    json_response = json.loads(response.text)
    
    if page:
        max_ergebnisse = json_response['maxErgebnisse']
        stellenangebote = json_response['maxErgebnisse']
        return stellenangebote, max_ergebnisse, size
    else:
        job_keys = list(job_response.keys())
        return json_response, job_keys

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
    'Projektmanager',
    ]

base_url = "https://rest.arbeitsagentur.de/"
jobboerse = "jobboerse/jobsuche-service/pc/v4/jobs?angebotsart=1&was="
fertigkeiten_count = 0
joblistings = []
listings_keys = []

for position in positions:
    joblist_url = f'{base_url}{jobboerse}{position}'
    page = 1
    page_bool = True
    while page_bool == True:
        stellenangebote, max_ergebnisse, size = get_page(joblist_url, page)
        if page == 1 and page_bool == True:
            page = (max_ergebnisse // size)+1
        else:
            if page == 2:
                page_bool = False
                break
            page -= 1

        i = 0
        for listing in stellenangebote:
            joblistings.append(listing)
            refnr = stellenangebote[i]['refnr']

            # encoding refnr to get the encoded job_id
            code_bytes = bytes(refnr, 'utf-8')
            encoded_code = b64encode(code_bytes)
            job_id = encoded_code.decode()

            job_url = f"{base_url}jobboerse/jobsuche-service/pc/v2/jobdetails/{job_id}"
            job_response, job_keys = get_page(job_url)
            
            for k in job_keys:
                listings_keys.append(k)
            
            # if 'externeUrl' in job_keys:
            #     pass
            # if 'fertigkeiten' in job_keys:
            #     # print(refnr, '\n')
            #     # print(job_keys, '\n')
            #     # print(job_json_response['fertigkeiten'], '\n')
            #     fertigkeiten_count += 1
            listing.update({'job_id':job_id})
            joblistings.append(listing)
            i += 1

    df_joblistings = pd.DataFrame(joblistings)
    # print(df_joblistings)
    # print(fertigkeiten_count)
    for value in set(listings_keys):
        print(value, '\n')