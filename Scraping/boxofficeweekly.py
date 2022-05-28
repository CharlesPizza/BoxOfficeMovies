import Scraping.constants as const
from bs4 import BeautifulSoup as bs
from random import randint
import numpy as np
import pandas as pd
import time
import lxml
import requests
import re

class WeeklyCharts():
    def __init__(self, start, stop, headers={'User-Agent': 'Mozilla/5.0'}):
        self.prefix = const.MOJO_WEEKLY_PRE
        self.date = float(start) - 0.01 #Decriment as we always get next value
        self.stop = float(stop)
        self.string_url = ''
        self.movie_dict = {}
        self.string_sfx = ''
        self.final_df = pd.DataFrame()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.teardown:
            self.quit()

    def string_suff(self):
    # URL suffix format is a 2 digit year, W, 2 digit week; starting at 20W01
    # Weeks start on friday. Converted to a float for ease of calculations
        string_sfx = str('{:.2f}'.format(self.date))
        string_sfx = string_sfx.replace('.','W')
        self.string_sfx = string_sfx
        return (string_sfx + '/')

    def next_page(self):
        if self.date == self.stop:
          return (self.stop)
        elif round(self.date % 1, ndigits=2) == 0.52:
          self.date += 1
          self.date -= 0.51
        else:
          self.date += .01
        self.string_url = self.prefix + self.string_suff()
        return self.string_url

    def crawl(self):
        while self.date < self.stop:
            time.sleep(randint(1,2)) #Provide pause to prevent throtteling
            page = requests.get(self.next_page(), 
                headers={'User-Agent': 'Mozilla/5.0'})
            soup = bs(page.text, 'lxml')
            table = soup.table.children
            for i in table:
                movie_name = i.find('a').text
                movie_url = i.find('a')['href']
                if movie_name not in self.movie_dict.keys():
                    self.movie_dict[movie_name] = movie_url
            #Quick yearweek workaround to circumvent odd structure of
            #friday to thursday week format. Needs restructure to
            # datetimes with timedelta alterations
            df = pd.read_html(page.text)
            df = df[0]
            df['YRWK'] = '{:2f}'.format(self.date) 
            self.final_df = pd.concat([self.final_df, df])
            print(f'{self.date}, {df.iloc[0, 2]}')

    def save_final_df(self):
        self.final_df.to_csv(f'WeeklyChartsDataFrame.csv')

    def save_movie_urls(self):
        url_df = pd.DataFrame.from_dict(self.movie_dict, orient='index')
        url_df.to_csv('Movie_url_list.csv')