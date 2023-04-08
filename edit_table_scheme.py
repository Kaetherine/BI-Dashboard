#%%
import pymysql
import pandas as pd
from credentials import user, password

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
for index, row in df_fertigkeit.iterrows():
    if index < 20:
        temp = {}
        temp['refnr'] = row[0]
        temp['beruf'] = row[1]
        temp['kategorie'] = row[2]
        if ',' in row[3] and '(' not in row[3]:
            fertigkeiten = row[3].split(',')
            for fertigkeit in fertigkeiten:
                temp[fertigkeit] = 1
        else:
            temp[row[3]] = 1
        df_fertigkeit_new.append(temp)
    else:
        break

#%%
df_fertigkeit_new = pd.DataFrame(df_fertigkeit_new)
df_fertigkeit_new.to_excel('df_fertigkeit.xlsx')

