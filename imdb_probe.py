from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import numpy as np
import re

class Boxy(webdriver.Chrome):
    def __init__(self, URL = 'https://pro.imdb.com/title/tt7975244/boxoffice',
        teardown = False):
        self.teardown = teardown
        self.title_ref = self.clean_url(URL)
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        super(Boxy, self).__init__(options=options)
        self.implicitly_wait(10)

    def __enter__(self):
        return self 

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.teardown:
            self.quit()

    def clean_url(self,URL):
        title_pattern = re.compile('/title/[a-z]+\d+/')
        title_ref = title_pattern.search(URL).group(0)
        return (title_ref)

    def land_page(self):
       self.get('https://www.imdb.com/'+self.title_ref)

    def get_rating_cert(self):
        try:
            # get a tag w/ rating
            rating = self.find_element(By.CSS_SELECTOR,
                'a[href*="parentalguide/certificates"]'
                ).get_attribute("innerHTML")
            return rating
        except NoSuchElementException:
            return 'Not Found'

    def get_budget(self):
        try:
            budget = self.find_element(By.CSS_SELECTOR,
                'li[data-testid="title-boxoffice-budget"]'
                ).text
            return budget
        except NoSuchElementException:
            budget = np.nan
            return budget

    def get_gross_domestic(self):
        try:
            gross_domestic = self.find_element(By.CSS_SELECTOR,
                'li[data-testid="title-boxoffice-grossdomestic"]'
                ).text
        except NoSuchElementException:
            return np.nan
        finally:
            return gross_domestic

    def get_gross(self):
        gross = self.find_element(By.CSS_SELECTOR,
            'li[data-testid="title-boxoffice-cumulativeworldwidegross"]'
            ).text
        return gross

    def get_gross_international(self):
        pass

