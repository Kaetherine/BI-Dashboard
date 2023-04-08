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
print(df_fertigkeit)
