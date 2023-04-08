#%%
import pymysql
import pandas as pd

#%%
connection = pymysql.connect(
                        host='localhost',
                        user='Katherine',
                        password='root',
                        db='bi_dashboard_db'
                        )
query = 'select * from fertigkeit;'

df_fertigkeit = pd.read_sql(query, con=connection)
print(df_fertigkeit)
