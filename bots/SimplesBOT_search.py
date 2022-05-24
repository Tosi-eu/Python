from openpyxl import Workbook
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import xlrd

driver = webdriver.Chrome('C:/Users/Usuario/Desktop/Curso/WebScrapping/chromedriver')
workbook = xlrd.open_workbook('C:/Users/Usuario/Desktop/Curso/WebScrapping/receitas.xls')
sheet = workbook.sheet_by_name('Planilha1')
rows = sheet.nrows
columns = sheet.ncols

options = webdriver.ChromeOptions()
options.add_argument("--disable-logging")
options.add_argument("--log-level=3")

driver.get('https://www.tudoreceitas.com/')

for curr_row in range(0, rows):
    x = sheet.cell_value(curr_row, 0) #reading each cell in row
    time.sleep(1)
    search = driver.find_element_by_id("q")
    time.sleep(1)
    search.clear()
    search.send_keys(x)
    time.sleep(1)
    search.send_keys(Keys.RETURN)
    time.sleep(2)

