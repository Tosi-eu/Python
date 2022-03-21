from selenium import webdriver
from selenium.webdriver.common.by import By
from datetime import datetime
import time
import pywhatkit as kit
import flask

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
# vaga_dia0 = driver.find_element(By.XPATH, '//*[@id="div-horarios"]/table/tbody/tr[3]/td[3]')


# vaga_dia6 = driver.find_element(By.XPATH, '//*[@id="div-horarios"]/table/tbody/tr[3]/td[3]')

while True:

    if datetime.today().weekday() == 0:
        vaga_dia1 = driver.find_element(By.XPATH,
                                        '//*[@id="div-horarios"]/table/tbody/tr[2]/td[3]')  # verficar vagas do dia
        if vaga_dia1.text != '10':
            driver.find_element(By.XPATH, '//*[@id="div-horarios"]/table/tbody/tr[2]/td[4]/button').click()
            time.sleep(2)
            kit.sendwhatmsg("+5519988640319", "Agendei o pilates", 12, 41)
            driver.close()
            break
        else:
            kit.sendwhatmsg("+5519988640319", "Turma está lotada nesse horário que eu tentei agendar o pilates", 12, 52)
            driver.close()

    if datetime.today().weekday() == 6:
        vaga_dia1 = driver.find_element(By.XPATH,
                                        '//*[@id="div-horarios"]/table/tbody/tr[3]/td[3]')  # verficar vagas do dia
        if vaga_dia1.text != '10':
            driver.find_element(By.XPATH, '//*[@id="div-horarios"]/table/tbody/tr[3]/td[4]/button').click()
            time.sleep(2)
            kit.sendwhatmsg("+5519988640319", "Agendei o pilates", 12, 41)
            driver.close()
            break
        else:
            kit.sendwhatmsg("+5519988640319", "Turma está lotada nesse horário que eu tentei agendar o pilates", 12, 52)
            driver.close()
            time.sleep(600)
# ----------------------------------------------------------------------------------------------------------------------
