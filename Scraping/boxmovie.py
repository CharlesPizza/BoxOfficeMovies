import re
import requests
import lxml
import pandas as pd
import time
import numpy as np
from bs4 import BeautifulSoup as bs
from random import randint
import Scraping.constants as const
from imdb_probe import Boxy


class MoviePage():
    def __init__(self, movie='The Wasp Woman', url_sfx='/title/tt0054462/'):
        self.name = movie
        self.url_sfx = url_sfx
        self.gross_pattern  = re.compile(r'.+(mojo-performance-summary-table$)')
        self.budget_pattern  = re.compile(r'Budget')
        self.mpaa_pattern  = re.compile(r'MPAA')
        self.genre_pattern  = re.compile(r'Genres')
        self.dictionary_row = {}

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print(f'Execution Type {exc_type}')
        print(f'Exc val {exc_val}')
        print(f'Exc Trace {exc_tb}')

    
    def __repr__(self):
        return(f'{self.name} has a url of {self.url_sfx}')

    def input_movie(self, movie, url_sfx):
        self.name = movie
        self.url_sfx = url_sfx

    def url_clean(self, sfx):
        clean_url = sfx.split('?')
        return clean_url[0]

    def crawl(self):
        gross_list = []
        time.sleep(randint(2, 3))
        page = requests.get(const.MOJO_PRE + self.url_sfx,
            headers={'User-Agent': 'Mozilla/5.0'})
        soup = bs(page.text, 'lxml')
        self.dictionary_row['Budget'] = self.get_budget(soup)
        self.dictionary_row['MPAA'] = self.get_mpaa(soup)
        self.dictionary_row['Genre'] = self.get_genre(soup)
        gross_list = self.get_gross(soup)
        self.dictionary_row['D.Gross'] = gross_list[0]
        self.dictionary_row['I.Gross'] = gross_list[1]
        self.dictionary_row['Total Gross'] = gross_list[2]
        if (self.dictionary_row['Budget'] is np.nan
            or self.dictionary_row['MPAA'] == 'Not Found'):
            self.probe_imdb(soup)
        self.check_rerelease(soup)

    def check_rerelease(self, soup):
        if re.match('Re-release', soup.get_text()):
            self.dictionary_row['']
        else:
            return True

    def get_budget(self, soup):
        try:
            budget = soup.find(text=self.budget_pattern).next_element
            budget_amount = int(re.sub('[$,]', '', budget.text))
        except AttributeError:
            budget_amount = np.nan
        return(budget_amount)

    def get_mpaa(self, soup):
        try:
            mpaa = soup.find(text=self.mpaa_pattern).next_element.text
        except AttributeError:
            mpaa = 'Not Found'
        return mpaa.strip()

    def get_genre(self, soup):
        try:
            genre = soup.find(
                text=self.genre_pattern).next_element.text.split()
            return(genre)
        except AttributeError:
            return ('attrerror')

    def get_gross(self, soup):
        grosses = soup.find(class_='mojo-performance-summary-table')
        money_pattern = re.compile('\$[\d+,]+|–')
        grosses = grosses.find_all('span', text=money_pattern)
        for idx, gross in enumerate(grosses):
            if gross.text == '–':
                grosses[idx] = np.nan
                continue
            else:
                grosses[idx] = int(re.sub('[$,]', '', gross.text))
        return(grosses)

    def probe_imdb(self, soup):
        pattern = re.compile('/title/.{2}\d+/')
        title_ref = soup.find('a', href=pattern)['href']
        with Boxy(URL=title_ref) as probe:
            probe.land_page()
            if self.dictionary_row['Budget'] is np.nan:
                try:
                    probe.get_budget()
                except AttributeError:
                    print(f'Error Occured. {self.name}, Budget, probe_imdb')
            if self.dictionary_row['MPAA'] == 'Not Found':
                try:
                    self.dictionary_row['MPAA'] = probe.get_rating_cert()
                except AttributeError:
                    print(f'Error Occured. {self.name}, MPAA, probe_imdb')