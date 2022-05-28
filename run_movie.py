#load url_list
from Scraping.boxmovie import MoviePage
import pandas as pd
df = pd.read_csv('Movie_url_list.csv')
df.columns = ['Name', 'URL']
# drop superfluous indexing remnant
df.drop(0, inplace=True)
# Convert to dictionary
movie_dict = df.set_index('Name').to_dict()
# Dict Shape is {URL: {, , , , , , }}
movie_dict = movie_dict['URL']
# Dict shape is now singular {, , , , }
series_dict = {}
with MoviePage() as release:
    for movie in movie_dict.keys():
        release.input_movie(movie=movie, url_sfx=movie_dict[movie])
        release.crawl()
        series_dict[release.name] = release.dictionary_row
        print(self.name)
        print(f'{release.dictionary_row}')

# save everything
new_df = pd.DataFrame.from_dict(series_dict, orient='index')
new_df.to_csv('MoviePerformance.csv')
print('yay!')