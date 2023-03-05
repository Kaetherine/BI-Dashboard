#%%
from datetime import datetime
import json
import pandas as pd
import requests
from sqlalchemy import create_engine
from base64 import b64encode

#%%
def get_page(url, page = False, size = 100):
    if page:
        url = f'{url}&page={page}&size={size}&pav=false'
    try:
        response = requests.get(url)
    except Exception as e:
        raise(e)
    json_response = json.loads(response.text)
    
    if page:
        try:
            max_ergebnisse = json_response['maxErgebnisse']
            stellenangebote = json_response['stellenangebote']
        except Exception as e:
            raise(e)
        return stellenangebote, max_ergebnisse, size
    else:
        job_keys = list(json_response.keys())
        return json_response, job_keys

#%%
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
    # 'Projektmanager',
    ]

# %%
base_url = "https://rest.arbeitsagentur.de/"
extended_url = "jobboerse/jobsuche-service/pc/v4/jobs?angebotsart=1&was="
joblist = []

for position in positions:
    joblist_url = f'{base_url}{extended_url}{position}'
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
            refnr = listing['refnr']

            # encoding refnr to get the encoded job_id
            code_bytes = bytes(refnr, 'utf-8')
            encoded_code = b64encode(code_bytes)
            job_id = encoded_code.decode()
            joblist.append({
                            'refnr' : listing['refnr'],
                            'job_id': job_id
                            })
            
#%%
fertigkeiten = []
i = 0
df_joblist = pd.DataFrame(joblist).drop_duplicates()
for job_id in df_joblist['job_id']:
    extended_url = 'jobboerse/jobsuche-service/pc/v2/jobdetails/'
    job_url = f'{base_url}{extended_url}{job_id}'
    job_response, job_keys = get_page(job_url)

    if 'externeUrl' in job_keys:
        pass
    if 'fertigkeiten' in job_keys:
        fertigkeiten.append({
            'refnr' : df_joblist['refnr'][i],
            'fertigkeiten' : job_response['fertigkeiten'] # Erinnerung: für jede fertigkeit eine spalte mit ausprägung als wert
        })
    i += 1
df_fertigkeiten = pd.DataFrame(fertigkeiten)
print(df_fertigkeiten)