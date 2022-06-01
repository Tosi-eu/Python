from ssl import Options
from webbrowser import Chrome
from pandas import options
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from time import sleep

class Youtubot():
  def __init__(self):
    options  = webdriver.ChromeOptions()
    options.add_argument("--disable-logging")
    options.add_argument("--log-server=3")
    self.webdriver = webdriver.Chrome("C:/Users/Usuario/Desktop/Curso/WebScrapping/chromedriver.exe", options=options)

  def search(self, subject, pages):
    page = 1
    url = f"https://www.youtube.com/results?search_query={subject}"
    self.webdriver.get(url)
    while page <= pages:
        titles_found = self.webdriver.find_elements(By.XPATH, "//*[@id='video-title']")
        for title in titles_found:
            print(f"Video found: {title.text}")
            print(f"Link: {title.get_attribute('href')}\n")
        page += 1
        if(page == pages):
            print("turning off in 3 seconds, search finished 8)")
            for seconds in range(3, 0, -1):
              print(f"{seconds}")
              sleep(1)
            self.webdriver.quit()
        else:
            self.next_page(page)

  def next_page(self, page):
      print(f"Turning page, to the page {page + 1}")
      bottom = page * 10000 #value necessary for turning page
      self.webdriver.execute_script(f"window.scrollTo(0, {bottom})")
      sleep(2)


bot = Youtubot()
bot.search("tesdey", 5) #enter with the search, and the number of pages that you want to get the videos titles
