from dotenv import load_dotenv
load_dotenv()
from datetime import datetime
import sqlite3
import numpy as np

import os
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.common.exceptions import (
    NoSuchElementException)



URL = "https://www.wsj.com/"
ARG_WINDOW_SIZE = "--window-size=1920,1080"

class Scraper:
    def __init__(self):
        self.url = URL
        self.driver = self.create_driver()

    def _create_options(self):
        self.chrome_options = Options()
        self.chrome_options.add_argument(ARG_WINDOW_SIZE)
        prefs = {"profile.managed_default_content_settings.images": 2}
        self.chrome_options.add_experimental_option("prefs", prefs)
        return self.chrome_options

    def create_driver(self):
        self._create_options()
        driver = webdriver.Chrome()
        driver.get(URL)
        return driver

class Search4Articles(Scraper):
    def __init__(self):
        super().__init__()
        self.user = os.environ.get("USER")
        self.pw = os.environ.get("PASS")
        
        self.db_name = 'articlesWSJ.db'
        
        self.link_index = 7

    
    def signin_fx(self):
        time.sleep(10) #Time to click the cookies

        #####################
        sign_in_link = self.driver.find_element(By.LINK_TEXT, "Sign In")
        sign_in_link.click()
        time.sleep(2)
        
        #####################
        username_0 = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.ID, "username"))
        )
        username_0.send_keys(self.user)
        time.sleep(2)
    
        submit_button_0 = self.driver.find_element(By.XPATH, ".//button[@type='button'][@class='solid-button continue-submit new-design']")
        submit_button_0.click()
        time.sleep(2)
        
        """
        future warning, make a conditional statement in case this is empty.
        
        username = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.ID, "password-login-username"))
        )
        """
        
        password = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.ID, 'password-login-password')))
        password.send_keys(self.pw)
        time.sleep(3)

        submit_button = self.driver.find_element(By.XPATH, ".//button[@type='submit'][@class='solid-button new-design basic-login-submit']")
        submit_button.click()
        time.sleep(3)
        
    def get_webpages_links(self, n_web):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM articles_index WHERE scanned_status = 0") #get list of not scanned
        rows = cursor.fetchall()
        conn.close()

        if rows and len(rows) >= n_web:
            links = np.array([[row[0], row[self.link_index]] for row in rows])
            pp = np.random.choice(len(rows), n_web)
            random_links = links[pp]
            return random_links

        else:
            print("No rows found where scanned_status is 0.")
            
    def insert_elements(self, elements):
        
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            cursor.execute("INSERT INTO article ('image_src', 'scanned_time', 'title', 'sub_title', 'corpus', 'index_id') VALUES (?, ?, ?, ?, ?, ?)",
                  (elements['image_src'], elements['scanned_time'], elements['title'], elements['sub_title'], elements['corpus'], elements['index_id']))
            conn.commit()
            print("Registered")

            row_id = elements['index_id']
            new_update_status = 1
        
            cursor.execute("UPDATE articles_index SET scanned_status = ? WHERE id = ?", (new_update_status, row_id))
            conn.commit()
            conn.close()
            print("Updated")
            
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")

        return 0
    
    def get_corpus(self):
        try:
            h1_element = self.driver.find_element(By.CSS_SELECTOR, "h1.css-1lvqw7f-StyledHeadline.e1ipbpvp0")
            h1_text = h1_element.text
        except NoSuchElementException:
            h1_text = 'not found'

        try:
            h2_element = self.driver.find_element(By.CSS_SELECTOR, "h2.css-jiugt2-Dek-Dek.e1jnru6p0")
            h2_text = h2_element.text
        except NoSuchElementException:
            h2_text = 'not found'

        try:
            section_element = self.driver.find_element(By.CSS_SELECTOR, "section.ef4qpkp0.css-y2scx8-Container.e1of74uw18")
            section_content = section_element.text
        except NoSuchElementException:
            section_content = 'not found'

        image_links = []

        # This block assumes that 'section_element' was successfully found; otherwise, skip it
        if section_content != 'not found':
            try:
                img_elements = section_element.find_elements(By.TAG_NAME, "img")
                for img_element in img_elements:
                    img_src = img_element.get_attribute('src')
                    if img_src:  # Check if 'src' attribute is not empty
                        image_links.append(img_src)
            except NoSuchElementException:
                image_links = 'not found'
        
        

        return h1_text, h2_text, section_content, image_links
    
    def navigation(self, n_web):
        list_webs = self.get_webpages_links(n_web)
        for web in list_webs:
            print(f'index {web[0]} web {web[1]}')
            self.driver.get(web[1])
            h1_text, h2_text, section_content, image_links = self.get_corpus()
            
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            dict_elements = {
                'image_src': str(image_links),
                'scanned_time': current_time,
                'title': h1_text,
                'sub_title': h2_text,
                'corpus' : str(section_content),
                'index_id': web[0],
            }
            self.insert_elements(dict_elements)
            
            time.sleep(10)


if __name__ == "__main__":
    start_time = time.time()
    n_web = 10 #Number of webpages to scrap
    sa =  Search4Articles() #Initiate
    sa.signin_fx() #Function to signin
    sa.navigation(n_web) #Get the webpages to scrap and call the function to scrap.
    print("End")
    