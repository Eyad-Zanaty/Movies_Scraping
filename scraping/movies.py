import random
import time
from selenium import webdriver
from fake_useragent import UserAgent
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import csv
import os

class (webdriver.Chrome):
    def __init__(self, driver_path= "E:\seleniumdriver", teardown=False):
        self.driver_path = driver_path
        self.teardown = teardown
        ua= UserAgent()
        user_agent= ua.random
        options = webdriver.ChromeOptions()
        options.add_argument('http://{const.proxy}') # Replace with your proxy if needed
        options.add_argument(f'user-agent={user_agent}')
        options.add_argument("--disable-gpu")   
        # options.add_argument(r'--user-data-dir=C:\Path\To\Your\Chrome\Default')
        options.add_argument('--disable-blink-features=AutomationControlled')
        os.environ['PATH'] += self.driver_path
        super(job_filtration, self).__init__(options=options)
        
    def __exit__(self, exc_type, exc, traceback):
        if self.teardown:
            self.quit()
        
    def open_site(self, url):
        self.get(url)  # Replace with the URL to site you want to scrape
        self.maximize_window()
        self.implicitly_wait(10)

    def top_movies(self):
        menu= self.find_element(By.ID, 'imdbHeader-navDrawerOpen').click()
        time.sleep(random.randint(1, 5))
        top_movies= self.find_element(By.XPATH, '//*[@id="imdbHeader"]/div/aside[1]/div/div[2]/div/div[1]/span/div/div/ul/a[2]/span').click()
        self.implicitly_wait(10)
        
    def top_movies_list(self):
        time.sleep(random.randint(1, 5))
        counter= 0
        movie_list= []
        self.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(random.randint(1, 5))
        movies_ul= self.find_element(By.CSS_SELECTOR, 'ul.ipc-metadata-list.ipc-metadata-list--dividers-between.sc-e22973a9-0.khSCXM.compact-list-view.ipc-metadata-list--base')
        movies= movies_ul.find_elements(By.TAG_NAME, 'li')
        for movie in movies:
            name= movie.find_element(By.CSS_SELECTOR, 'a.ipc-title-link-wrapper').text
            name= name.split(' ')[1:]
            name= " ".join(name)
            production_year= movie.find_element(By.CSS_SELECTOR, 'div.sc-86fea7d1-7.iqovgP.cli-title-metadata').text[:4]
            duration= movie.find_element(By.CSS_SELECTOR, 'div.sc-86fea7d1-7.iqovgP.cli-title-metadata').text[4:-1]
            ratings= movie.find_element(By.CSS_SELECTOR, 'span.ipc-rating-star--rating').text
            movie_list.append({
                'name': name,
                'production_year': production_year,
                'duration': duration,
                'ratings': ratings
            })
            counter += 1
            if counter % 3 == 0:
                time.sleep(random.randint(1, 2))
                
        return movie_list
        
    def save_to_files(self, movie_list):
            os.makedirs('data', exist_ok=True)
            with open(r'data\top_movies.txt', 'w') as t:
                for movie in movie_list:
                    t.write(f"Name: {movie['name']}\n")
                    t.write(f"Production Year: {movie['production_year']}\n")
                    t.write(f"Duration: {movie['duration']}\n")
                    t.write(f"Ratings: {movie['ratings']}\n\n")
                print("Data saved to top_movies.txt")
                t.close()
            
            with open(r'data\top_movies.json', 'w') as j:
                json.dump(movie_list, j, ensure_ascii=False, indent=4)
                print("Data saved to top_movies.json")
                j.close()
                
            with open(r'data\top_movies.csv', 'w', newline='') as c:
                writer = csv.DictWriter(c, fieldnames=['name', 'production_year', 'duration', 'ratings'])
                writer.writeheader()
                writer.writerows(movie_list)
                print("Data saved to top_movies.csv")
                c.close()