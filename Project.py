import pandas as pd
import matplotlib.pyplot as plt
from prettytable import PrettyTable as pt
import os

# Function to remove special characters
def correct_names(name):
    name = name.replace('.', '').replace('ç', 'c').replace('ô', 'o').replace('é', 'e').replace('í', 'i').replace('ê', 'e').replace('ã', 'a').replace('ó', 'o').replace('ú', 'u').replace('á', 'a')
    return name

# Hello everyone, it's a great pleasure to have you seeing my project, and seeking knowledge
# This project is an analysis of a fictitious company that my teacher built

# All of these first commands are to prepare the PyCharm for improve all the analysis
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)

clients_df = pd.read_csv('CadastroClientes.csv', sep=';')
functionary_df = pd.read_csv(r'CadastroFuncionarios.csv', sep=';', decimal=',')
services_df = pd.read_excel('BaseServiçosPrestados.xlsx')

# Step 0: Apply function correct names on the three dataframes, on the columns that we need
# (columns with names specifically, 'cause there are names with special characters

clients_df['Cliente'] = clients_df['Cliente'].apply(correct_names)
functionary_df['Nome Completo'] = functionary_df['Nome Completo'].apply(correct_names)

# Step 1: create a payroll of this company using the 'CadastroFuncionarios' data

functionary_df['Salary including all benefits'] = functionary_df['Salario Base'] + functionary_df['Impostos'] + \
                                                  functionary_df['Beneficios'] + functionary_df['VT'] + functionary_df[
                                                      'VR']

total = functionary_df['Salary including all benefits'].sum()

# Step 2: Do merge() for create a company billing

billing_df = services_df[['ID Cliente', 'Tempo Total de Contrato (Meses)']].merge(
    clients_df[['ID Cliente', 'Valor Contrato Mensal']], on='ID Cliente')
billing_df['Total Billing'] = billing_df['Tempo Total de Contrato (Meses)'] * billing_df['Valor Contrato Mensal']
billing = billing_df['Total Billing'].sum()
# print(billing)

# Step 3: Remove all duplicates from the services table with the unique() function

contract_employees = len(services_df['ID Funcionário'].unique())
total_employees = len(functionary_df['ID Funcionário'])
percent = (contract_employees / total_employees) * 100
# print(f'{round(percent, 2)}%')

# Step 4: Each area has 'n' contracts, we have to count them, removing all duplicates, we have to merge the employees'
# table with the services table, and then we go utilise value.counts()

contracts_df = services_df[['ID Funcionário']].merge(functionary_df[['ID Funcionário', 'Area']], on='ID Funcionário')
contracts_df = contracts_df['Area'].value_counts()
contracts_df = dict(contracts_df)
# print(contracts_df)

x = pt()
x.field_names = ['Work Area', 'Amount of Contracts']
x.add_row(['Administrative', contracts_df['Administrativo']])
x.add_row(['Operations', contracts_df['Operações']])
x.add_row(['Commercial', contracts_df['Comercial']])
x.add_row(['Financial', contracts_df['Financeiro']])
x.add_row(['Logistics', contracts_df['Logística']])

# OBS: I'll make put each row using pretty table library

# Step 5: Employees x Area, it's simpler than the last step, we only have to apply value_counts() on 'Area' column of
# 'CadastroFuncionarios'

employees_areas = functionary_df['Area'].value_counts()

"""plt.figure(1, figsize=(10, 12))
plt.title('| Step 5 : Total employees in each area |')
employees_areas.plot(kind='bar')
plt.show()
"""

# Step 6: Calculate average ticket, so we will use mean() in the 'CadastroClientes' table

mean_clients = clients_df['Valor Contrato Mensal'].mean()
round(mean_clients, 2)
# print(mean_clients)

# Step 7: Rename the columns and value in rows to portuguese into english

clients_df = clients_df.rename(columns={'ID Cliente': 'Client ID'}, inplace=False)
clients_df = clients_df.rename(columns={'Cliente': 'Client'}, inplace=False)
clients_df = clients_df.rename(columns={'Valor Contrato Mensal': 'Contract Value (Monthly)'}, inplace=False)

functionary_df = functionary_df.rename(columns={'ID Funcionário': 'Employee ID'}, inplace=False)
functionary_df = functionary_df.rename(columns={'Estado Civil': 'Marital Status'}, inplace=False)
functionary_df = functionary_df.rename(columns={'Nome Completo': 'Full Name'}, inplace=False)
functionary_df = functionary_df.rename(columns={'Salario Base': 'Base Wage(Reais)'}, inplace=False)
functionary_df = functionary_df.rename(columns={'Impostos': 'Taxes'}, inplace=False)
functionary_df = functionary_df.rename(columns={'Beneficios': 'Benefits'}, inplace=False)
functionary_df = functionary_df.rename(columns={'VT': 'TV'}, inplace=False)
functionary_df = functionary_df.rename(columns={'VR': 'MT'}, inplace=False)
functionary_df = functionary_df.rename(columns={'Cargo': 'Office'}, inplace=False)
functionary_df = functionary_df.rename(columns={'SEX': 'Sex'}, inplace=False)
functionary_df = functionary_df.rename(columns={'Area': 'Area'}, inplace=False)

services_df = services_df.rename(columns={'Codigo do Servico': 'Service Code'}, inplace=False)
services_df = services_df.rename(columns={'ID Funcionário': 'Employee ID'}, inplace=False)
services_df = services_df.rename(columns={'ID Cliente': 'Client ID'}, inplace=False)
services_df = services_df.rename(columns={'Tempo Total de Contrato (Meses)': 'Monthly Time of Contract (In Months)'},
                                 inplace=False)

functionary_df['Area'] = functionary_df['Area'].replace(['Operações'], ['Operations'])
functionary_df['Area'] = functionary_df['Area'].replace(['Logística'], ['Logistics'])
functionary_df['Area'] = functionary_df['Area'].replace(['Administrativo'], ['Administrative'])
functionary_df['Area'] = functionary_df['Area'].replace(['Financeiro'], ['Financial'])
functionary_df['Area'] = functionary_df['Area'].replace(['Comercial'], ['Commerce'])

functionary_df['Office'] = functionary_df['Office'].replace(['Diretor'], ['Director'])
functionary_df['Office'] = functionary_df['Office'].replace(['Estagiário'], ['Trainee'])
functionary_df['Office'] = functionary_df['Office'].replace(['Analista'], ['Analyst'])
functionary_df['Office'] = functionary_df['Office'].replace(['Coordenador'], ['Coordinator'])
functionary_df['Office'] = functionary_df['Office'].replace(['Gerente'], ['Manager'])

functionary_df['Marital Status'] = functionary_df['Marital Status'].replace(['C'], ['Married'])
functionary_df['Marital Status'] = functionary_df['Marital Status'].replace(['S'], ['Single'])

services_df = services_df.rename(columns={'Codigo do Servico': 'Service Code'}, inplace=False)
services_df = services_df.rename(columns={'ID Funcionário': 'Employee ID'}, inplace=False)
services_df = services_df.rename(columns={'ID Cliente': 'Client ID'}, inplace=False)
services_df = services_df.rename(columns={'Tempo Total de Contrato (Meses)': 'Total Contract Time (Months)'},
                                 inplace=False)

# Step 8: Create a menu with options to see the tables until the stop point is triggered
# Firstly, create a tuple with all operators

interval = (1, 2, 3, 4, 5)

while True:

    print('=-'*25)
    print(' 1 - See the DataFrame of Clients Registration')
    print(' 2- See the DataFrame of Employees Registration')
    print(' 3 - See the DataFrame of Base of Services Provided')
    print(' 4 - See a graph and a table of total employees per area')
    print(' 5 - See a graph of total employees per area')
    print('=-' * 25)

    print()
    op = int(input('Choose an option: '))

    if op == 1:
        print(clients_df)
    elif op == 2:
        print(functionary_df)
    elif op == 3:
        print(services_df)
    elif op == 4:
        print(x)
    elif op == 5:
        plt.figure(1, figsize=(10, 12))
        plt.title('| Step 5 : Total employees in each area |')
        employees_areas.plot(kind='bar')
        plt.show()

    else:
        while True:
            op3 = int(input('Invalid option, try again: '))

            if op3 == 1:
                print(clients_df)
            elif op3 == 2:
                print(functionary_df)
            elif op3 == 3:
                print(services_df)
            elif op3 == 4:
                print(x)
            elif op3 == 5:
                plt.figure(1, figsize=(10, 12))
                plt.title('| Step 5 : Total employees in each area |')
                employees_areas.plot(kind='bar')
                plt.show()

                if op3 in interval:
                    break

    question = str(input('Do you want to continue [Anything/N]?: ')).upper()[0]
    os.system('cls')

    if question in 'N':
        break

# Step 9: Save the dataframes into new others datafrmes

services_df.to_excel('BaseOfServicesProvided.xlsx')
functionary_df = functionary_df.to_csv('EmployeesRegistration.csv')
clients_df = clients_df.to_csv('ClientsRegistration.csv')