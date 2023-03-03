from datetime import datetime
import json
import pandas as pd
import requests
from sqlalchemy import create_engine
from base64 import b64encode
import time

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

job_specs = [
    'befristungDatum',
    'eintrittsdatum',
    'sonstigesAusbildung',
    'fuerFluechtlingeGeeignet',
    'anzahlOffeneStellen',
    'fuehrungskompetenzen',
    'allianzpartnerUrl',
    'arbeitgeberdarstellung',
    'beruf',
    'usbildungen',
    'arbeitgeberLogoHashId',
    'titel',
    'berufserfahrung',
    'istPrivateArbeitsvermittlung',
    'arbeitgeberAdresse',
    'arbeitgeberdarstellungUrl',
    'aktuelleVeroeffentlichungsdatum',
    'ersteVeroeffentlichungsdatum',
    'nurFuerSchwerbehinderte',
    'logref',
    'externeUrl',
    'alternativBerufe',
    'laufzeitBis',
    'anzeigeAnonym',
    'branche',
    'istZeitarbeit',
    'uebernahme',
    'chiffrenummer',
    'istGoogleJobsRelevant',
    'betriebsgroesse',
    'arbeitgeberHashId',
    'stellenbeschreibung',
    'refnr',
    'staerken',
    'arbeitsorte',
    'allianzpartner',
    'tarifvertrag',
    'timestamp',
    'messages',
    'befristungDauer',
    'branchengruppe',
    'mobilitaet',
    'modifikationsTimestamp',
    'arbeitszeitmodelle',
    'fertigkeiten',
    'hauptDkz',
    'alternativDkzs',
    'hashId',
]

base_url = "https://rest.arbeitsagentur.de/"
jobboerse = "jobboerse/jobsuche-service/pc/v4/jobs?angebotsart=1&was="
page_nav = "&page=1&size=25&pav=false"

fertigkeiten_count = 0
joblistings = []
listings_keys = []
for position in positions:
    time.sleep(1)
    joblist_url = f'{base_url}{jobboerse}{position}{page_nav}'
    try:
        response = requests.get(joblist_url)
    except KeyError:
        pass
    json_response = json.loads(response.text)

    i = 0
    
    for listing in json_response['stellenangebote']:
        time.sleep(1)
        joblistings.append(listing)
        refnr = json_response['stellenangebote'][i]['refnr']

        code_bytes = bytes(refnr, 'utf-8')
        encoded_code = b64encode(code_bytes)
        job_id = encoded_code.decode()

        job_url = f"{base_url}jobboerse/jobsuche-service/pc/v2/jobdetails/{job_id}"
        job_response = requests.get(job_url)
        job_json_response = json.loads(job_response.text)
        job_keys = list(job_json_response.keys())
        
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