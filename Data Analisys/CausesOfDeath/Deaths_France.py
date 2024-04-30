import pandas as pd
import os
from prettytable import PrettyTable

df = pd.read_csv(r'CausesOfDeath_France_2001-2008.csv', sep=',')

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)

# Columns with NaN
df = df.drop('Flag and Footnotes', axis=1)
# if value is ':', remove it
df.drop(df.loc[df['Value'] == ':'].index, inplace=True)

# new data frame with split value columns
lista_df = df["Value"].str.split(" ", n=1, expand=True)

lista_df_0 = lista_df[0]
lista_df_1 = lista_df[1]
sum_deaths = 0

lista_df_1 = lista_df_1.replace([None], [''])

result = []
for n1, n2 in zip(lista_df_0, lista_df_1):
    result.append(n1 + n2)

# returning a list to df['Value']
df['Value'] = result

# Converting str values to int
df['Value'] = df['Value'].astype(int)

# New columns with highest, lowest and absolute values, and changing NaN to 0
df.loc[(df['Value'] >= 10000) & (df['Value'] < 250788), 'Highest Values'] = df['Value']
df['Highest Values'] = df['Highest Values'].fillna(0)
df['Highest Values'] = df['Highest Values'].astype(int)

df.loc[df['Value'] < 10000, 'Lowest Values'] = df['Value']
df['Lowest Values'] = df['Lowest Values'].fillna(0)
df['Lowest Values'] = df['Lowest Values'].astype(int)

df.loc[df['Value'] >= 250788, 'Absolute Values'] = df['Value']
df['Absolute Values'] = df['Absolute Values'].fillna(0)
df['Absolute Values'] = df['Absolute Values'].astype(int)

# Rename column of diseases 'cause TIME will not make sense after sum()
df = df.rename(columns={'ICD10': 'ICD10 (From 2001-2008)'}, inplace=False)

# Removing this column 'cause after sum(), the years will be insignificant
# Removing all columns of All deaths 'cause it is unnecessary
# Removing AGE column 'cause it's irrelevant for not having enough data

df = df.drop('AGE', axis=1)
df = df.drop('UNIT', axis=1)
df = df.drop(0)
df = df.drop(66)
df = df.drop(132)
df = df.drop(198)
df = df.drop(264)
df = df.drop(330)
df = df.drop(396)
df = df.drop(462)
df = df.drop(528)
df = df.drop(594)
df = df.drop(660)
df = df.drop(726)
df = df.drop(792)
df = df.drop(858)
df = df.drop(924)
df = df.drop(990)

# Excluding total deaths and creating a counter of deaths
sum_deaths = df['Value']
df.loc[1, 'Absolute Values'] = sum_deaths.sum()

# Time has an error when sum() is called, so converting to str, it's solved
df = df.rename(columns={'TIME': 'Year'}, inplace=False)
df = df.rename(columns={'GEO': 'Place'}, inplace=False)
df = df.rename(columns={'SEX': 'Sex'}, inplace=False)
df['Year'] = df['Year'].astype(str)

# Max and min values of each year
max_2001 = df[df['Year'] == '2001']
max_2002 = df[df['Year'] == '2002']
max_2003 = df[df['Year'] == '2003']
max_2004 = df[df['Year'] == '2004']
max_2005 = df[df['Year'] == '2005']
max_2006 = df[df['Year'] == '2006']
max_2007 = df[df['Year'] == '2007']
max_2008 = df[df['Year'] == '2008']

v_2001 = max_2001['Value'].max()
v_2002 = max_2002['Value'].max()
v_2003 = max_2003['Value'].max()
v_2004 = max_2004['Value'].max()
v_2005 = max_2005['Value'].max()
v_2006 = max_2006['Value'].max()
v_2007 = max_2007['Value'].max()
v_2008 = max_2008['Value'].max()

vl_2001 = max_2001['Value'].min()
vl_2002 = max_2002['Value'].min()
vl_2003 = max_2003['Value'].min()
vl_2004 = max_2004['Value'].min()
vl_2005 = max_2005['Value'].min()
vl_2006 = max_2006['Value'].min()
vl_2007 = max_2007['Value'].min()
vl_2008 = max_2008['Value'].min()

# This part is for take the row with the data of each year with the highest number of deaths
bigger_2001 = df.loc[(df['Year'] == '2001') & (df['Value'] == v_2001)]
lesser_2001 = df.loc[(df['Year'] == '2001') & (df['Value'] == vl_2001)]
bigger_2001 = bigger_2001.drop(columns='Highest Values')
bigger_2001 = bigger_2001.drop(columns='Lowest Values')
bigger_2001 = bigger_2001.drop(columns='Absolute Values')
lesser_2001 = lesser_2001.drop(columns='Highest Values')
lesser_2001 = lesser_2001.drop(columns='Lowest Values')
lesser_2001 = lesser_2001.drop(columns='Absolute Values')
# print(bigger_2001)

bigger_2002 = df.loc[(df['Year'] == '2002') & (df['Value'] == v_2002)]
lesser_2002 = df.loc[(df['Year'] == '2002') & (df['Value'] == vl_2002)]
bigger_2002 = bigger_2002.drop(columns='Highest Values')
bigger_2002 = bigger_2002.drop(columns='Lowest Values')
bigger_2002 = bigger_2002.drop(columns='Absolute Values')
lesser_2002 = lesser_2002.drop(columns='Highest Values')
lesser_2002 = lesser_2002.drop(columns='Lowest Values')
lesser_2002 = lesser_2002.drop(columns='Absolute Values')

# print(bigger_2002)

bigger_2003 = df.loc[(df['Year'] == '2003') & (df['Value'] == v_2003)]
lesser_2003 = df.loc[(df['Year'] == '2003') & (df['Value'] == vl_2003)]
bigger_2003 = bigger_2003.drop(columns='Highest Values')
bigger_2003 = bigger_2003.drop(columns='Lowest Values')
bigger_2003 = bigger_2003.drop(columns='Absolute Values')
lesser_2003 = lesser_2003.drop(columns='Highest Values')
lesser_2003 = lesser_2003.drop(columns='Lowest Values')
lesser_2003 = lesser_2003.drop(columns='Absolute Values')
# print(bigger_2003)

bigger_2004 = df.loc[(df['Year'] == '2004') & (df['Value'] == v_2004)]
lesser_2004 = df.loc[(df['Year'] == '2004') & (df['Value'] == vl_2004)]
bigger_2004 = bigger_2004.drop(columns='Highest Values')
bigger_2004 = bigger_2004.drop(columns='Lowest Values')
bigger_2004 = bigger_2004.drop(columns='Absolute Values')
lesser_2004 = lesser_2004.drop(columns='Highest Values')
lesser_2004 = lesser_2004.drop(columns='Lowest Values')
lesser_2004 = lesser_2004.drop(columns='Absolute Values')
# print(bigger_2004)

bigger_2005 = df.loc[(df['Year'] == '2005') & (df['Value'] == v_2005)]
lesser_2005 = df.loc[(df['Year'] == '2005') & (df['Value'] == vl_2005)]
bigger_2005 = bigger_2005.drop(columns='Highest Values')
bigger_2005 = bigger_2005.drop(columns='Lowest Values')
bigger_2005 = bigger_2005.drop(columns='Absolute Values')
lesser_2005 = lesser_2005.drop(columns='Highest Values')
lesser_2005 = lesser_2005.drop(columns='Lowest Values')
lesser_2005 = lesser_2005.drop(columns='Absolute Values')
# print(bigger_2005)

bigger_2006 = df.loc[(df['Year'] == '2006') & (df['Value'] == v_2006)]
lesser_2006 = df.loc[(df['Year'] == '2006') & (df['Value'] == vl_2006)]
bigger_2006 = bigger_2006.drop(columns='Highest Values')
bigger_2006 = bigger_2006.drop(columns='Lowest Values')
bigger_2006 = bigger_2006.drop(columns='Absolute Values')
lesser_2006 = lesser_2006.drop(columns='Highest Values')
lesser_2006 = lesser_2006.drop(columns='Lowest Values')
lesser_2006 = lesser_2006.drop(columns='Absolute Values')
# print(bigger_2006)

bigger_2007 = df.loc[(df['Year'] == '2007') & (df['Value'] == v_2007)]
lesser_2007 = df.loc[(df['Year'] == '2007') & (df['Value'] == vl_2007)]
bigger_2007 = bigger_2007.drop(columns='Highest Values')
bigger_2007 = bigger_2007.drop(columns='Lowest Values')
bigger_2007 = bigger_2007.drop(columns='Absolute Values')
lesser_2007 = lesser_2007.drop(columns='Highest Values')
lesser_2007 = lesser_2007.drop(columns='Lowest Values')
lesser_2007 = lesser_2007.drop(columns='Absolute Values')
# print(bigger_2007)

bigger_2008 = df.loc[(df['Year'] == '2008') & (df['Value'] == v_2008)]
lesser_2008 = df.loc[(df['Year'] == '2008') & (df['Value'] == vl_2008)]
bigger_2008 = bigger_2008.drop(columns='Highest Values')
bigger_2008 = bigger_2008.drop(columns='Lowest Values')
bigger_2008 = bigger_2008.drop(columns='Absolute Values')
lesser_2008 = lesser_2008.drop(columns='Highest Values')
lesser_2008 = lesser_2008.drop(columns='Lowest Values')
lesser_2008 = lesser_2008.drop(columns='Absolute Values')
# print(bigger_2008)

# Returning a value to a variable, considering the exact year
df_2001 = df.loc[df['Year'] == '2001', ['Value']].sum(axis=1)
df_2001.fillna(0, inplace=True)
df_2001 = df_2001.sum()

df_2002 = df.loc[df['Year'] == '2002', ['Value']].sum(axis=1)
df_2002.fillna(0, inplace=True)
df_2002 = df_2002.sum()

df_2003 = df.loc[df['Year'] == '2003', ['Value']].sum(axis=1)
df_2003.fillna(0, inplace=True)
df_2003 = df_2003.sum()

df_2004 = df.loc[df['Year'] == '2004', ['Value']].sum(axis=1)
df_2004.fillna(0, inplace=True)
df_2004 = df_2004.sum()

df_2005 = df.loc[df['Year'] == '2005', ['Value']].sum(axis=1)
df_2005.fillna(0, inplace=True)
df_2005 = df_2005.sum()

df_2006 = df.loc[df['Year'] == '2006', ['Value']].sum(axis=1)
df_2006.fillna(0, inplace=True)
df_2006 = df_2006.sum()

df_2007 = df.loc[df['Year'] == '2007', ['Value']].sum(axis=1)
df_2007.fillna(0, inplace=True)
df_2007 = df_2007.sum()

df_2008 = df.loc[df['Year'] == '2008', ['Value']].sum(axis=1)
df_2008.fillna(0, inplace=True)
df_2008 = df_2008.sum()

sum_deaths = df_2001 + df_2002 + df_2003 + df_2004 + df_2005 + df_2006 + df_2007 + df_2008

# Doing a table showing the total of deaths in each year, and the sum of all of them
x = PrettyTable()

x.field_names = ["Year", "Value"]

x.add_row(['2001', df_2001])
x.add_row(['2002', df_2002])
x.add_row(['2003', df_2003])
x.add_row(['2004', df_2004])
x.add_row(['2005', df_2005])
x.add_row(['2006', df_2006])
x.add_row(['2007', df_2007])
x.add_row(['2008', df_2008])
x.add_row(['TOTAL', sum_deaths])

# Returning all content of the df in each year, and distributing in 8 variables different
df_2001 = df[df['Year'] == '2001']
df_2002 = df[df['Year'] == '2002']
df_2003 = df[df['Year'] == '2003']
df_2004 = df[df['Year'] == '2004']
df_2005 = df[df['Year'] == '2005']
df_2006 = df[df['Year'] == '2006']
df_2007 = df[df['Year'] == '2007']
df_2008 = df[df['Year'] == '2008']

# Tuple for the operands
interval = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12)

df.to_csv(r"CausesOfDeath_France_2001-2008_2.csv", sep=',')

while True:
    # Menu
    print('=-' * 20)
    print()
    print('           WHICH AN OPTION')
    print('1 - See All the DATAFRAME')
    print('2 - See the data of 2001')
    print('3 - See the data of 2002')
    print('4 - See the data of 2003')
    print('5 - See the data of 2004')
    print('6 - See the data of 2005')
    print('7 - See the data of 2006')
    print('8 - See the data of 2007')
    print('9 - See the data of 2008')
    print('10 - See the total deaths in each year')
    print('11 - More deaths per year')
    print('12 - Fewer deaths per year')
    print()
    print('=-' * 20)

    op = int(input('Choose your option: '))
    os.system('cls')

    if op == 1:
        print(df)
    elif op == 2:
        print(df_2001)
    elif op == 3:
        print(df_2002)
    elif op == 4:
        print(df_2003)
    elif op == 5:
        print(df_2004)
    elif op == 6:
        print(df_2005)
    elif op == 7:
        print(df_2006)
    elif op == 8:
        print(df_2007)
    elif op == 9:
        print(df_2008)
    elif op == 10:
        print(x)
    elif op == 11:
        print(f'{bigger_2001}\n\n{bigger_2002}\n\n{bigger_2003}\n\n{bigger_2004}\n\n{bigger_2005}\n\n{bigger_2006}\n\n'
              f'{bigger_2007}\n\n{bigger_2008}')
    elif op == 12:
        print(f'{lesser_2001}\n\n{lesser_2002}\n\n{lesser_2003}\n\n{lesser_2004}\n\n{lesser_2005}\n\n'
              f'{lesser_2006}\n\n{lesser_2007}\n\n{lesser_2008}\n\n')

    if op not in interval:
        while True:
            op3 = int(input('Invalid option, try again: '))
            os.system('cls')

            if op == 1:
                print(df)
            elif op == 2:
                print(df_2001)
            elif op == 3:
                print(df_2002)
            elif op == 4:
                print(df_2003)
            elif op == 5:
                print(df_2004)
            elif op == 6:
                print(df_2005)
            elif op == 7:
                print(df_2006)
            elif op == 8:
                print(df_2007)
            elif op == 9:
                print(df_2008)
            elif op == 10:
                print(x)
            elif op == 11:
                print(
                    f'{bigger_2001}\n\n{bigger_2002}\n\n{bigger_2003}\n\n{bigger_2004}\n\n{bigger_2005}\n\n{bigger_2006}'
                    f'\n\n{bigger_2007}\n\n{bigger_2008}')
            elif op == 12:
                print(f'{lesser_2001}\n\n{lesser_2002}\n\n{lesser_2003}\n\n{lesser_2004}\n\n{lesser_2005}\n\n'
                      f'{lesser_2006}\n\n{lesser_2007}\n\n{lesser_2008}\n\n')
            break

    question = str(input('Do you want to continue [Anything/N]?: ')).upper()[0]
    os.system('cls')

    if question in 'N':
        break
