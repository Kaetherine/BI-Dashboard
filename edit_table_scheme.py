#%%
import pymysql
import pandas as pd
from credentials import user, password
from datetime import datetime
from sqlalchemy import create_engine
import pandas as pd

#%%
connection = pymysql.connect(
                        host='localhost',
                        user=user,
                        password=password,
                        db='newschema'
                        )


#%%
query = 'select * from fertigkeit;'
df_fertigkeit = pd.read_sql(query, con=connection)
df_fertigkeit = df_fertigkeit.drop('auspraegung', axis=1)

# print(df_fertigkeit)

#%%
fertigkeit_new = []
for index, row in df_fertigkeit.iterrows():
    temp = {}
    temp['refnr'] = row[0]
    temp['beruf'] = row[1]
    temp['beruf_kategorie'] = row[2]
    temp['fertigkeit_kategorie'] = row[3]

    if '3d' in row[3].lower():
        temp['3D'] = 1
        temp[fertigkeit.replace('-', '').replace('/', ' ').strip().lower()] = 1
    if 'jpa' in row[3].lower() or 'soap' in row[3].lower() or 'benutzerschnittstellen' in row[3].lower() or 'api' in row[3].lower():
        temp['api'] = 1
        temp[fertigkeit.replace('-', '').replace('/', ' ').strip().lower()] = 1
    if 'content-management-system' in row[3].lower():
        temp['cms'] = 1
    if 'crm' in row[3].lower():
        temp['crm'] = 1
        temp[fertigkeit.replace('-', '').replace('/', ' ').strip().lower()] = 1
    if 'warenwirtschaft' in row[3].lower() or ('enterprise' in row[3].lower() and 'ressource' in row[3].lower() and 'planning' in row[3].lower()):
        temp['erp'] = 1
    if 'e-mail-programm' in row[3].lower() or 'outlook' in row[3].lower():
        temp['e-mail-programm'] = 1
    if 'ecm' in row[3].lower() or 'enterprise-content-management' in row[3].lower():
        temp['ecm'] = 1
    if 'design' in row[3].lower():
        temp['design'] = 1
    if 'informations-' in row[3].lower():
        temp[row[3]] = 1
    if 'internet of things' in row[3].lower():
        temp['iot'] = 1
    if 'local area network' in row[3].lower():
        temp['lan'] = 1
    if 'kosten- und leistungsrechnung' in row[3].lower():
        temp['kosten- und leistungsrechnung'] = 1
    if 'key-account-management' in row[3].lower() or 'großkundenbearbeitung' in row[3].lower():
        temp['key-account-management'] = 1
    if 'ms ' in row[3].lower() or 'microsoft' in row[3].lower() or '365' in row[3].lower():
        temp['microsoft'] = 1
    if 'office' in row[3].lower() or '365' in row[3].lower():
        temp['office programm'] = 1
    if 'oo-programmierung' in row[3].lower() or 'objektorientierte' in row[3].lower():
        temp['oop'] = 1
    if 'personal' in row[3].lower():
        temp['personalwesen'] = 1
    if 'präsentationsprogramm' in row[3].lower() or 'powerpoint' in row[3].lower() or 'pp' in row[3].lower():
        temp['präsentationssoftware'] = 1
    if 'product-lifecycle-management' in row[3].lower():
        temp['plm'] = 1
    if 'software' in row[3].lower():
        temp['software'] = 1
    if 'projektmanagement' in row[3].lower():
        temp['projektmanagement'] = 1
    if 'sap' in row[3].lower():
        temp['sap'] = 1
    if 'rest' in row[3].lower():
        temp['rest'] = 1
    if 'unified modeling language' in row[3].lower():
        temp['uml'] = 1
    if 'virtual private network' in row[3].lower():
        temp['vpn'] = 1
    if 'user interface' in row[3].lower():
        temp['ui'] = 1
    if 'business intelligence' in row[3].lower():
        temp['business intelligence'] = 1
    if 'technisches verständnis' in row[3].lower():
        temp['technisches verständnis'] = 1
    
    if ',' in row[3] and '(' not in row[3]:
        fertigkeiten = row[3].split(',')
        for fertigkeit in fertigkeiten:
            fertigkeit = fertigkeit.replace('(', '').replace(')', '').replace(',', '').lower().strip()
            temp[fertigkeit.replace('-', '').replace('/', ' ').strip().lower()] = 1
    
    if ',' not in row[3]:
        for fertigkeit in row[3].split():
            fertigkeit = fertigkeit.replace('(', '').replace(')', '').replace(',', '').lower().strip()
    fertigkeit_new.append(temp)
connection.close()

#%%
df_fertigkeit_new = pd.DataFrame(fertigkeit_new)

#%% df ordnen
sorted_cols = sorted(df_fertigkeit_new.columns[1:], key=lambda x: len(df_fertigkeit_new[x]), reverse=True)
new_cols = ["refnr", "beruf", "beruf_kategorie", "fertigkeit_kategorie"] + sorted_cols
df = df_fertigkeit_new[new_cols]
# print(df)

#%% df in db eintragen
engine = create_engine('mysql+pymysql://' + user + ':' + password + '@localhost/newschema')
df_fertigkeit_new.to_sql('fertigkeit', con=engine, if_exists='replace', index=False)
engine.dispose()
print('done')

