from selenium import webdriver
from selenium.webdriver.common.by import By
from datetime import datetime
import time

url = 'https://www.agendaftc.com.br/login'
driver = webdriver.Chrome()
driver.get(url)
time.sleep(4)

# ----------------------------------------------------------------------------------------------------------------------
                                                        # login
driver.find_element(By.XPATH, "/html/body/div[3]/div/div/div[2]/form/div/div[1]/input").send_keys('silviacgt@gmail.com')
time.sleep(2)
driver.find_element(By.XPATH, '/html/body/div[3]/div/div/div[2]/form/div/div[2]/input').send_keys('@Confidencial10')
time.sleep(2)
# ----------------------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------
                                 # agendamento de atividades e clicar em pilates

driver.find_element(By.XPATH, '/html/body/div[3]/div/div/div[2]/form/div/div[3]/button').click()
time.sleep(2)
driver.find_element(By.XPATH, '//*[@id="colorlib-main-menu"]/ul/li[4]/a').click()
time.sleep(2)
# ----------------------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------
                                           # clicar no dia da semana
driver.find_element(By.XPATH, '//*[@id="colorlib-main"]/div[1]/div/div[4]/div[20]/button').click()
time.sleep(2)
driver.find_element(By.XPATH, '/html/body/div/div/div[2]/div/div/div[2]/div[1]/div[2]/button').click()
time.sleep(2)
# ----------------------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------
                                     # armazenar dado e verificar se tem vaga
vaga = driver.find_element(By.XPATH, '//*[@id="div-horarios"]/table/tbody/tr[3]/td[3]')

while True:

    dia = datetime.today().weekday()

    if dia == 0:
        if vaga.text == '10':
            # print('Lotado!')
            time.sleep(600)
        else:
            driver.find_element(By.XPATH, '//*[@id="div-horarios"]/table/tbody/tr[3]/td[4]/button').click()
            # print('Agendado!')
            driver.close()
            break
    else:
        break
# ----------------------------------------------------------------------------------------------------------------------
