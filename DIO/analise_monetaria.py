# -*- coding: utf-8 -*-
"""Análise Monetária.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1qvBOsWiZ5K0ERFAcqnLl7rSEsh6Zkr0I
"""

import pandas as pd
import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter, FormatStrFormatter

df = pd.read_csv("table1.csv")
plt.style.use('seaborn-v0_8-paper')

#traduzindo o nome das colunas e removendo algumas menos relevantes
#TODO: webscrapping da coação atual do dólar, criar novas colunas em reais
df.drop(columns=["Median weekly earnings (in constant dollars) - Total", "Median weekly earnings (in constant dollars) - Men", "Median weekly earnings (in constant dollars) - Women"], inplace=True)

df.rename(columns={
    "Year": "Ano",
    "Quarter": "Trimestre",
    "Number of workers (in thousands) - Total": "Número total de trabalhadores",
    "Number of workers (in thousands) - Men": "Número total de homens trabalhando",
    "Number of workers (in thousands) - Women": "Número total de mulheres trabalhando",
    "Median weekly earnings (in current dollars) - Total": "Ganho médio semanal (cotação atual $$)",
    "Median weekly earnings (in current dollars) - Men": "Ganho médio semanal masculino (cotação atual $$)",
    "Median weekly earnings (in current dollars) - Women": "Ganho médio semanal feminino (cotação atual $$)",
    }, inplace=True)

#testada. Retorno o valor atual do dólar, arrendodado em 2 casas decimais (com tratamento de exceção)
def dollar_quotation(url, html_structure, attrs:dict):
  try:
    content = requests.get(url)
    bs = BeautifulSoup(content.content, "html.parser")
    response = bs.find_all(html_structure, attrs=attrs)[0]
  except Exception as e:
    return e
  finally:
    return round(float(response.text), 2)

dollar = dollar_quotation("https://www.cnbc.com/quotes/BRL=", "span", {'class': 'QuoteStrip-lastPrice'})

df["Ganho médio semanal, em R$"] = df["Ganho médio semanal (cotação atual $$)"]*dollar
df["Ganho médio semanal masculino, em R$"] = df["Ganho médio semanal masculino (cotação atual $$)"]*dollar
df["Ganho médio semanal feminino, em R$"] = df["Ganho médio semanal feminino (cotação atual $$)"]*dollar

#para analisar cada semestre de maneira individual, ordenar a planilha com base no trimestre e ano (o contrário dificulta a visualização)
df.sort_values(by=["Trimestre", "Ano"], inplace=True)
df

#trimestre é int, não precisamos tratar (visualizado com df.dtypes)
first_quarter = df[df['Trimestre'] == 1]
second_quarter = df[df['Trimestre'] == 2]
third_quarter = df[df['Trimestre'] == 3]
fourth_quarter = df[df['Trimestre'] == 4]

#função para pegar o maior valor por trimestre do período todo
def get_max_num_per_quarter(values:list):
  return max(values)

def get_min_num_per_quarter(values:list):
  return min(values)

#tratando o número total de trabalhadores, no caso, estavam como string, o correto seria float/double
employees_first_quarter = round(first_quarter["Número total de trabalhadores"].str.replace(',', '').astype(float).sum(), 2) #955104.0
employees_second_quarter = round(second_quarter["Número total de trabalhadores"].str.replace(',', '').astype(float).sum(), 2) #960879.0
employees_third_quarter = round(third_quarter["Número total de trabalhadores"].str.replace(',', '').astype(float).sum(), 2) #965023.0
employees_fourth_quarter = round(fourth_quarter["Número total de trabalhadores"].str.replace(',', '').astype(float).sum(), 2) #1067842.0

#de fato retorna o número máximo e vê-se que corresponde ao quarto semestre do período todo
max_employees = get_max_num_per_quarter([employees_first_quarter, employees_second_quarter, employees_third_quarter, employees_fourth_quarter])
max_employees

min_employees = get_min_num_per_quarter([employees_first_quarter, employees_second_quarter, employees_third_quarter, employees_fourth_quarter])
min_employees

# plot
plt.ticklabel_format(style='plain', axis='both')
x=[employees_first_quarter, employees_second_quarter, employees_third_quarter, employees_fourth_quarter]
y=[1, 2, 3, 4]
plt.yticks(y, labels=[str(v) for v in y])
plt.gca().yaxis.set_major_locator(plt.MultipleLocator(0.5))
plt.xlabel("Número de trabalhadores")
plt.ylabel("Trimestre")
plt.title("Trabalhadores x Trimestre")
plt.stem(x, y)
plt.show()

#salário masculino - não precisa de tratamento pois já está como float
employees_male_salary_first_quarter = round(first_quarter["Ganho médio semanal masculino (cotação atual $$)"].astype(float).sum(), 2)
employees_male_salary_second_quarter = round(second_quarter["Ganho médio semanal masculino (cotação atual $$)"].astype(float).sum(), 2)
employees_male_salary_third_quarter = round(third_quarter["Ganho médio semanal masculino (cotação atual $$)"].astype(float).sum(), 2)
employees_male_salary_fourth_quarter = round(fourth_quarter["Ganho médio semanal masculino (cotação atual $$)"].astype(float).sum(), 2)

# plot
plt.ticklabel_format(style='plain', axis='both')
x=[employees_male_salary_first_quarter, employees_male_salary_second_quarter, employees_male_salary_third_quarter, employees_male_salary_fourth_quarter]
y=[1, 2, 3, 4]
plt.yticks(y, labels=[str(v) for v in y])
plt.gca().yaxis.set_major_locator(plt.MultipleLocator(0.5))
plt.xlabel("Salário")
plt.ylabel("Trimestre")
plt.title("Salário masculino x Trimestre")
plt.stem(x, y)
plt.show()

#salário feminino
employees_female_salary_first_quarter = round(first_quarter["Ganho médio semanal feminino (cotação atual $$)"].astype(float).sum(), 2)
employees_female_salary_second_quarter = round(second_quarter["Ganho médio semanal feminino (cotação atual $$)"].astype(float).sum(), 2)
employees_female_salary_third_quarter = round(third_quarter["Ganho médio semanal feminino (cotação atual $$)"].astype(float).sum(), 2)
employees_female_salary_fourth_quarter = round(fourth_quarter["Ganho médio semanal feminino (cotação atual $$)"].astype(float).sum(), 2)

# plot
plt.ticklabel_format(style='plain', axis='both')
x=[employees_female_salary_first_quarter, employees_female_salary_second_quarter, employees_female_salary_third_quarter, employees_female_salary_fourth_quarter]
y=[1, 2, 3, 4]
plt.yticks(y, labels=[str(v) for v in y])
plt.gca().yaxis.set_major_locator(plt.MultipleLocator(0.5))
plt.xlabel("Salário")
plt.ylabel("Trimestre")
plt.title("Salário feminino x Trimestre")
plt.stem(x, y)
plt.show()

# plot
plt.ticklabel_format(style='plain', axis='both')
x=[employees_female_salary_first_quarter / 9, employees_female_salary_second_quarter / 9
, employees_female_salary_third_quarter / 9, employees_female_salary_fourth_quarter / 10]
y=[1, 2, 3, 4]
plt.yticks(y, labels=[str(v) for v in y])
plt.gca().yaxis.set_major_locator(plt.MultipleLocator(0.5))
plt.xlabel("Média salarial")
plt.ylabel("Trimestre")
plt.title("Média de salaŕio feminino x Trimestre")
plt.stem(x, y)
plt.show()

# plot
plt.ticklabel_format(style='plain', axis='both')
x=[employees_male_salary_first_quarter / 9, employees_male_salary_second_quarter / 9
, employees_male_salary_third_quarter / 9, employees_male_salary_fourth_quarter / 10]
y=[1, 2, 3, 4]
plt.yticks(y, labels=[str(v) for v in y])
plt.gca().yaxis.set_major_locator(plt.MultipleLocator(0.5))
plt.xlabel("Média salarial")
plt.ylabel("Trimestre")
plt.title("Média de salaŕio masculino x Trimestre")
plt.stem(x, y)
plt.show()
