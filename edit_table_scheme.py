#%%
import pymysql
import pandas as pd
from credentials import user, password
from datetime import datetime
from fertigkeiten_evaluation import * 

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

#buzzwords mit geringer häufigkeit finden
buzzwords = {}
df_buzzwords = []
excluded_from_buzzwords = ['und', 'nach', 'oder', '/', '(', ')', '.', '-', '_', 'u.a.)', 'u.a.']
excluded_from_splitting = ['und', 'nach', 'oder', '/', '(', ')', '.', '-', '_', 'u.a.)', 'u.a.']

ok_new = []
pruefen_new = []

for index, row in df_fertigkeit.iterrows():
    # temp = {}
    # temp['refnr'] = row[0]
    # temp['beruf'] = row[1]
    # temp['kategorie'] = row[2]
    temp_l = []
    if 'enterprise' in row[3].lower():
        temp_l.append(row[3])
    for value in set(temp_l):
        print(value)

    # for fertigkeit in row[3].split():
    #     fertigkeit = fertigkeit.replace('(', '').replace(')', '').replace(',', '').lower().strip() #!!
    #     if fertigkeit in excluded_from_buzzwords:
    #         continue
    #     elif fertigkeit not in buzzwords.keys():
    #         buzzwords[fertigkeit] = 1
    #         if 'office' in row[3]:
    #             buzzwords['office programm'] = 1
    #         elif 'programmieren' in row[3]:
    #             continue
    #         elif 'business intelligence' in row[3]:
    #             buzzwords['business intelligence'] = 1

    #         else:
    #             buzzwords[fertigkeit] += 1

# #
# for index, row in df_fertigkeit.iterrows():
#     temp = {}
#     temp['refnr'] = row[0]
#     temp['beruf'] = row[1]
#     temp['kategorie'] = row[2]
#     if ',' in row[3] and '(' not in row[3]:
#         fertigkeiten = row[3].split(',')
#         for fertigkeit in fertigkeiten:
#             fertigkeit
#             temp[fertigkeit] = 1
#     elif 'programmiersprache' in row[3].lower() and 'programmiersprache c' != row[3].lower() and '/' not in row[3].lower():
#         fertigkeiten = row[3].split(' ')

#         for fertigkeit in fertigkeiten:
#             temp[fertigkeit] = 1
#     else:
#         temp[row[3]] = 1
#         for fertigkeit in row[3].split():

#             fertigkeit = fertigkeit.replace('(', '').replace(')', '').replace(',', '').lower().strip() #!!

#             if fertigkeit in excluded_from_buzzwords:
#                 continue
            

#             elif fertigkeit not in buzzwords.keys():
#                 buzzwords[fertigkeit] = 1
#             elif 'office' in fertigkeit:
#                 buzzwords['office programme'] = 1
#             elif 'programmieren' in fertigkeit:
#                 buzzwords['Programmiersprache'] = 1
#             elif 'business intelligence' in fertigkeit:
#                 buzzwords['business intelligence'] = 1
#             else:
#                 buzzwords[fertigkeit] += 1
#     df_fertigkeit_new.append(temp)

# #%%
# buzzwords = dict(sorted(buzzwords.items(), key=lambda x: -x[1]))
# df_buzzwords = pd.DataFrame(list(buzzwords.items()), columns=['Keys', 'Values'])

# # DataFrame in Excel exportieren
# df_buzzwords.to_excel('buzzwords.xlsx', index=False)
# # print(df_buzzwords)
# #%%
# # sorted_dict = dict(sorted(buzzwords.items(), key=lambda x: -x[1]))
# # sorted_dict_df = []
# # # print(sorted_dict)
# # for entry in sorted_dict:
# #     sorted_dict_df.append(entry)

# # # df_fertigkeit_new = pd.DataFrame(df_fertigkeit_new)
# # # df_fertigkeit_new.to_excel('df_fertigkeit.xlsx')
# # print(sorted_dict_df)
# # sorted_dict = pd.DataFrame(sorted_dict_df)
# # # print(sorted_dict)
# # sorted_dict.to_excel('buzzwords.xlsx')

