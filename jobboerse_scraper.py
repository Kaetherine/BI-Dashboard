#%%
import json
import logging
import math
import pandas as pd
import requests
from sqlalchemy import create_engine
from base64 import b64encode

#%%
logging.basicConfig(
    filename='logger.log',
    level = logging.DEBUG,
    format='%(asctime)s:%(levelname)s:%(message)s'
)

#%%
def get_page(url, page = False, size = 100):
    '''Takes the joblist and jobdetails url and returns its assets.'''
    if size > 100:
        size = 100
    if page:
        url = f'{url}&page={page}&size={size}&pav=false'
    try:
        response = requests.get(url)
    except Exception as e:
        logging.error(e)
        pass

    if response:
        json_response = json.loads(response.text)
        status = response.status_code
    
        if page:
            try:
                max_ergebnisse = json_response['maxErgebnisse']
                stellenangebote = json_response['stellenangebote']
            except Exception as e:
                logging.error(e)
                pass
            return stellenangebote, max_ergebnisse, size, status
        else:
            job_keys = list(json_response.keys())
            return json_response, job_keys, status
    else:
        pass

#%%
positions = [
    # 'SAP-Entwickler/SAP-Berater',
    # 'IT-Projektmanager',
    # 'Softwareentwickler',
    # 'Business Intelligence Analyst',
    'IT-Controller',
    # 'IT-Berater',
    # 'Produktmanager',
    # 'App-Entwickler',
    'Anwendungsentwickler',
    # 'Datenbankspezialist',
    # 'ERP Manager',
    'Data Analyst',
    # 'Data Scientist',
    # 'Data Engineer',
    # 'Projektmanager',
    ]

# %%
base_url = 'https://rest.arbeitsagentur.de/'
extended_url = 'jobboerse/jobsuche-service/pc/v4/jobs?angebotsart=1&was='
joblist = []

for position in positions:
    joblist_url = f'{base_url}{extended_url}{position}'
    page = 1
    page_bool = True
    while page_bool == True:
        stellenangebote, max_ergebnisse, size, status = get_page(
            joblist_url, page, 25
            )
        if status == 200:
            if page == 1 and page_bool == True:
                page = math.ceil((max_ergebnisse / size))
            else:
                if page == 2:
                    page_bool = False
                    pass
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
        else:
            pass
 
df_joblist = pd.DataFrame(joblist).drop_duplicates()
logging.info(f'{len(df_joblist)} items in df_joblist.')

#%%
fertigkeiten_dict = []
i = 0
for job_id in df_joblist['job_id']:
    extended_url = 'jobboerse/jobsuche-service/pc/v2/jobdetails/'
    job_url = f'{base_url}{extended_url}{job_id}'
    try:
        job_response, job_keys, status = get_page(job_url)
        status
    except Exception as e:
        logging.error(e)

    if 'externeUrl' in job_keys:
        pass
    if 'fertigkeiten' in job_keys:
        fertigkeiten_k = job_response['fertigkeiten'][0]['auspraegungen']
        try:
            refnr = df_joblist['refnr'][i]
        except Exception as e:
            logging.error(e)

        if refnr:
            temp = {}
            temp['refnr'] = refnr
            for k in fertigkeiten_k:
                for fertigkeit in fertigkeiten_k[k]:
                    # temp[fertigkeit] = k
                    temp[fertigkeit] = 1
            if 'titel' in job_keys:
                temp['titel'] = job_response['titel']
            if 'beruf' in job_keys:
                temp['beruf'] = job_response['beruf']
            if 'fuehrungskompetenzen' in job_keys:
                temp['fuehrungskompetenzen'] = job_response['fuehrungskompetenzen']
        fertigkeiten_dict.append(temp)
    i += 1

#%%
print(len(fertigkeiten_dict))
df_fertigkeiten = pd.DataFrame(fertigkeiten_dict)
df_fertigkeiten.to_excel('df_fertigkeiten.xlsx')
# %%
