from unicodedata import name
from matplotlib import scale
from matplotlib.font_manager import json_dump
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.ticker as plticker
import pandas as pd
import json

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)

URL = 'https://us-central1-raccoon-bi.cloudfunctions.net/psel_de_ingressos'
URL2 = 'https://us-central1-raccoon-bi.cloudfunctions.net/psel_de_compras'
URL3 = 'https://us-central1-raccoon-bi.cloudfunctions.net/psel_de_shows'

df = pd.read_json(URL)
df = df.sort_values(by=['nome']) # to get a better way of visualizing the data

df2 = pd.read_csv(URL2, sep=',')
df3 = pd.read_json(URL3)
df4 = pd.merge(df, df2, how='inner', left_on='nome', right_on='nome')

df_track = df4.loc[(df4['tipo'] == 'Pista')]
df_track_concluded = df4.loc[(df4['tipo'] == 'Pista') & (df4['status'] == 'Concluido')] # for analizing the difference beetween the mean of rows with 'pista' status and 'pista' and 'concluido' status

df_days = df4[(df4['status'] != 'Concluido')]
df_res = df_days.drop(df_days.columns[[0, 1, 2, 4, 5]], axis=1)

#1)
print('\nAmount cast without the concluded status: $${:.2f}\nAmount cast with concluded status: $${:.2f}'.format(df_track['gastos'].mean(), df_track_concluded['gastos'].mean()))
print()

#2)
 
 # -> all people went at any show 'cause everyone cast some money 

#3)
print('\nPeople that didnt buy tickets with AT: \n')
competitor_names = df4.loc[(df4['status'] != 'Concluido') & (df_res["gastos"] > 0), "nome"].drop_duplicates()
competitor_names = competitor_names.drop([18, 30, 83, 115, 162, 262, 282, 295, 324, 336]) # names with 'Concluido' and 'Nao Concluido' or 'Problema no pagamento' either
print(competitor_names)
print()

#4)
print('\nDay With biggest amount of casts: \n')
more_expensiveDay = (df4[['dia', 'gastos', 'status']].groupby('dia', as_index=False)).sum().sort_values(by='gastos', ascending=False)
print("Day {}: {}".format(more_expensiveDay['dia'][0], more_expensiveDay['gastos'][0]))
print()

# the graph helps us to verify that day 1 is the day where the people cast the biggest amount of money
fig = plt.figure()
fig = plt.xticks(np.arange(0, 5))
fig = plt.yticks(np.arange(0, 270000, 25000))
x = np.array([more_expensiveDay['dia'][0], more_expensiveDay['dia'][1], more_expensiveDay['dia'][2]])
y = np.array([more_expensiveDay['gastos'][0], more_expensiveDay['gastos'][1], more_expensiveDay['gastos'][2]])
plt.title("Money spent in shows")
plt.ylabel("Amount of money spent")
plt.xlabel("Days")
plt.bar(x,y)
plt.show()

#5)

competitor_names = df4.loc[(df4['status'] != 'Concluido') & (df_res["gastos"] > 0), "nome"].drop_duplicates()
competitor_names_for_show = df4.loc[(df4['status'] != 'Concluido') & (df_res["gastos"] > 0), ["nome", 'show']]
competitor_values = df4.loc[(df4['status'] != 'Concluido') & (df_res["gastos"] > 0), "gastos"].drop_duplicates()
competitor_values = df4.groupby('nome', as_index=False).sum()

competitor_names = competitor_names.drop([18, 30, 83, 115, 162, 262, 282, 295, 324, 336]) # names with 'Concluido' and 'Nao Concluido' or 'Problema no pagamento' either
competitor_values = competitor_values.drop([2, 5, 7, 8, 10, 12, 14, 16, 17,  21, 24, 27, 28, 31, 32, 33, 34, 36, 40, 42]) # names with 'Concluido' and 'Nao Concluido' or 'Problema no pagamento' either
competitor_show = competitor_names_for_show.drop(np.r_[18:35,83:98, 115:116, 162:173, 184:228, 262:266, 282:285, 295:315, 324:326,  336:345, 354:372]) #with groupby or lambda function, the array of lists was bigger than the others, so would be impossible to create the df
competitor_show = competitor_show.groupby('nome').apply(lambda grupo: grupo.show.tolist()).tolist()

dict_list = {'nome': [name for name in competitor_names], 'gastos': [value for value in competitor_values['gastos']], 'shows': [shows for shows in competitor_show]}

new_df = pd.DataFrame(data=dict_list)

result = new_df.to_json(orient='records')
parsed = json.loads(result)
print(json.dumps(parsed, indent=4))
