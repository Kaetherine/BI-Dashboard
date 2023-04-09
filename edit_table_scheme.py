#%%
import pymysql
import pandas as pd
from credentials import user, password
from datetime import datetime

#%%
connection = pymysql.connect(
                        host='localhost',
                        user=user,
                        password=password,
                        db='bi_dashboard_db'
                        )

#%%
query = 'select * from fertigkeit;'
df_fertigkeit = pd.read_sql(query, con=connection)
df_fertigkeit = df_fertigkeit.drop('auspraegung', axis=1)

# print(df_fertigkeit)

#%%
df_fertigkeit_new = []
buzzwords = {}
excluded_from_buzzwords = ['und', 'nach', 'oder', '/', '(', ')', '.', '-', '_', 'u.a.)', 'u.a.']
for index, row in df_fertigkeit.iterrows():
    temp = {}
    temp['refnr'] = row[0]
    temp['beruf'] = row[1]
    temp['kategorie'] = row[2]
    if ',' in row[3] and '(' not in row[3]:
        fertigkeiten = row[3].split(',')
        for fertigkeit in fertigkeiten:
            temp[fertigkeit] = 1
    elif 'Programmiersprache' in row[3] and 'Programmiersprache C' != row[3] and '/' not in row[3]:
        fertigkeiten = row[3].split(' ')
        for fertigkeit in fertigkeiten:
            temp[fertigkeit] = 1
    else:
        temp[row[3]] = 1
        for fertigkeit in row[3].split():
            fertigkeit = fertigkeit.replace('(', '').replace(')', '').replace(',', '').lower().strip()
            if fertigkeit in excluded_from_buzzwords:
                continue
            elif fertigkeit not in buzzwords.keys():
                buzzwords[fertigkeit] = 1
            else:
                buzzwords[fertigkeit] += 1
    df_fertigkeit_new.append(temp)

#%%
sorted_dict = dict(sorted(buzzwords.items(), key=lambda x: -x[1]))
sorted_dict_df = []
# print(sorted_dict)
for entry in sorted_dict:
    sorted_dict_df.append(entry)

# df_fertigkeit_new = pd.DataFrame(df_fertigkeit_new)
# df_fertigkeit_new.to_excel('df_fertigkeit.xlsx')
print(sorted_dict_df)
sorted_dict = pd.DataFrame(sorted_dict_df)
# print(sorted_dict)
sorted_dict.to_excel('buzzwords.xlsx')