# -*- coding: utf-8 -*-

from os import system
from bs4 import BeautifulSoup
from prettytable import PrettyTable
import requests
from time import sleep
from prettytable.colortable import ColorTable, Themes


url_bank = ['https://lista.mercadolivre.com.br/', 'https://www.gsuplementos.com.br/busca/?busca=', 'https://www.mithoficial.com.br/homens/todas-categorias/', 'https://pesquisa.marisa.com.br/busca?q=']


table = PrettyTable()
table = ColorTable(theme=Themes.OCEAN)

sleep(1)
system('clear')

table.field_names = ['Options','Sites']
table.add_row(['1', 'Mercado Livre'])
table.add_row(['2', 'Growth'])
table.add_row(['3', 'Mith'])
table.add_row(['4', 'Marisa'])

while True:

    print('-=-=-= WELCOME, STRANGER, TO THE WEB SCRAPPING PROGRAM -=-=-=\n')

    print(table)

    choose = int(input('\n-Choose the site for navigating: '))

    if choose == 1:
        url = str(url_bank[0])
    elif choose == 2:
        url = str(url_bank[1])
    elif choose == 3:
        url = str(url_bank[3])
    elif choose == 4:
        url = str(url_bank[2])
    else:
        print('ERROR')
  
    product = input('Product name: ') 

    response = requests.get(url + product)

    site_content = BeautifulSoup(response.text, 'html.parser')
    
    each_item_ml = site_content.findAll('div', attrs={'class': 'andes-card andes-card--flat andes-card--default ui-search-result ui-search-result--core andes-card--padding-default'})
    each_item_growth = site_content.findAll('div', attrs={'class': 'columns flex-container align-middle slider-vitrine-item categoriaProdItem listagem'})
    each_item_renner = site_content.findAll('li', attrs={'class': 'nm-product-item'})

    with open('Products_ml.csv', 'a') as file:

        if choose == 1:
            for product in each_item_ml:

                title = product.find('h2', attrs={'class': 'ui-search-item__title'})
                link_prod = product.find('a', attrs={'class': 'ui-search-link'})

                money_int = product.find('span', attrs={'class': 'price-tag-fraction'})
                money_float = product.find('span', attrs={'class': 'price-tag-cents'})
                
                print('- Produto: ' + title.text)
                file.write('- Produto: ' + title.text + '\n')

                print('- Link: ' + link_prod['href'])
                file.write('- Link: ' + link_prod['href'] + '\n')

                if money_float:
                    print(f'- Preço: R${money_int.text},{money_float.text}')
                    file.write(f'- Preço: R${money_int.text},{money_float.text}\n')
                else:
                    print(f'- Preço: R${money_int.text}')
                    file.write(f'- Preço: R${money_int.text}\n')

                print('\n\n')
                file.write('\n\n')

        elif choose == 2:
        
            with open('Products_growth.csv', 'a') as file:

                for product in (each_item_growth):

                    title = product.find('a', attrs={'class': "vitrine-nomeProduto"})
                    link_prod = product.find('a', attrs={'class': 'vitrine-nomeProduto'})
                    
                    print('- Produto: ' + title.text)
                    file.write('- Produto: ' + title.text)

                    money = product.find('span', attrs={'class': "vitrine-valor"})
                    money_card_full = product.find('span', attrs={'class': "vitrine-valorCartao"})
                    money_card_min = product.find('b')

                    print(money.text)
                    file.write(f'- Preço: {money.text} no boleto ou {money_card_min.text} no cartão.')
                    print(f'- Preço: {money.text} no boleto ou {money_card_min.text} no cartão.')

                    print('\n\n')
                    file.write('\n\n')

        elif choose == 3:

              with open('Products_Marisa.csv', 'a') as file:

                for product in (each_item_renner):

                        title = product.find('img', attrs={'class': 'nm-product-img'})
                        title_l = title['title']

                        link_prod = product.find('h4', attrs={'class': 'nm-product-name'})
                        link_l = link_prod.a['href']

                        price_prod = product.find('span', attrs={'class': 'price-number'})
                        
                        print(f'- Produto: {title_l}')
                        file.write(f'- Produto: {title_l}')
                        
                        print(f'- Link: {link_l}')
                        file.write(f'- Link: {link_l}')

                        print(price_prod.text)
                        file.write(f'- Preço: {price_prod.text} no boleto ou no cartão.')

                        print('\n\n')
                        file.write('\n\n')


    op = str(input('Continue? [Y/N]: ')).upper()

    if op == 'N':
        file.close()
        break

    if op not in 'YN':
         while op not in 'YN':
            op = str(input('Invalid operation, type again...Continue? [Y/N]: ')).upper()

         if op == 'Y':
            sleep(1)
            system('clear')
         else:
            file.close()
            break
    
