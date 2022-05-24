from base64 import urlsafe_b64decode
from lib2to3.pgen2 import driver
from selenium import webdriver
import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep

options = webdriver.ChromeOptions()
options.add_argument("--disable-logging")
options.add_argument("--log-level=3")

task = Service(ChromeDriverManager().install()) 
driver = webdriver.Chrome(service=task, options=options)
driver.get('https://www.google.com')

doubt = str(input("What do you want to search?: "))
search = driver.find_element(By.XPATH, "//input[@aria-label='Pesquisar']")
search.send_keys(doubt)
search.send_keys(Keys.RETURN)

results = driver.find_element(By.XPATH, '//*[@id="result-stats"]').text
print(results)

howMany_res = int(results.split('Aproximadamente')[1].split('resultados')[0].replace('.',''))

max_pages = howMany_res / 10

#print("Number of pages: %s"% (max_pages))

url_pages = driver.find_element(By.XPATH, '//a[@aria-label="Page 2"]').get_attribute('href')
actual_page = 0
start = 10
result_list = []

while actual_page <= 10:
      if not actual_page == 0:
          url_pages = url_pages.replace("start=%s" % start, "start=%s" % (start+10))
          start += 10
      actual_page += 1
      driver.get(url_pages)
  
      divs = driver.find_elements(By.XPATH, '//div[@class="g tF2Cxc"]')
      for div in divs:
            name = div.find_element(By.XPATH, '//h3[@class="LC20lb MBeuO DKV0Md"]')
            link = div.find_element(By.TAG_NAME, 'a')
            result = "%s;%s" % (name.text, link.get_attribute('href'))
            result_list.append(result)


with open("results_search.txt", "w") as file:
    for results in result_list:
            file.write("%s\n" % results)

file.close()


