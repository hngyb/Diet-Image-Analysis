from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException, NoSuchElementException
from time import sleep
import os
import requests
import sys

class PinterestScraper:
    def __init__(self, login_id, login_pwd):
        self.login_id = login_id
        self.login_pwd = login_pwd
        chromedriver_path = '/Applications/chromedriver'
        self.driver = webdriver.Chrome(executable_path = chromedriver_path)
        self.driver.get("https://www.pinterest.co.kr")
        
        self.driver.implicitly_wait(30)
    
    def login(self):
        self.driver.find_element_by_xpath('//*[@id="__PWS_ROOT__"]/div[1]/div/div/div/div[1]/div[1]/div[2]/div[2]/button').click()
        email = self.driver.find_element_by_name('id')
        email.send_keys(self.login_id)
        pwd = self.driver.find_element_by_name('password')
        pwd.send_keys(self.login_pwd)
        self.driver.find_element_by_xpath('//*[@id="__PWS_ROOT__"]/div[1]/div/div/div/div[1]/div[2]/div[2]/div/div/div/div[1]/div/div/div/div[3]/form/div[5]/button/div').click()
        

    def set_destination_folder(self, path):
        self.path = path
        self.scraped_list = os.listdir(self.path)

    def scrape_pictures(self, search_word ,n_pgdn):
        scrape_word = self.driver.find_element_by_name('searchBoxInput')
        scrape_word.send_keys(search_word)
        scrape_word.send_keys(Keys.ENTER)
        sleep(3)

    
        for i in range(n_pgdn):
            pics_list = self.driver.find_elements_by_tag_name('img')
            pics_list = pics_list[1:]
            pic_url_list = [pic_elem.get_attribute('srcset').split(' ')[-2] for pic_elem in pics_list]
            for pic_url in pic_url_list:
                pic_name = pic_url.split('/')[-1]
                pic = requests.get(pic_url)
                file = open(os.path.join(self.path, pic_name), 'wb')
                file.write(pic.content)
                file.close()
            body = self.driver.find_element_by_css_selector('body')
            for j in range(2):
                body.send_keys(Keys.PAGE_DOWN)
            sleep(2)

login_id = 'your ID'
login_pwd = 'yout Password'
myScraper = PinterestScraper(login_id, login_pwd)

myScraper.login()

path = 'A path where you save images'
myScraper.set_destination_folder(path)

search_word = 'your search key word'
myScraper.scrape_pictures(search_word, n_pgdn = 200)