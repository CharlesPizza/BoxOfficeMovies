# Webscraper for BoxOfficeMojo
This webcrawler is designed to iterate through BoxOfficeMojo's weekly boxoffice charts and aggregate a movie list. The webscraper collects information on each movie in the list as it navigates the website. BoxOfficeMojo's dynamic creation of the website makes it very accessible to scrape extremely valuable information which may be to the detriment of BoxOfficeMojo.

At the time of publication, all sites scraped permit webscrapers in all areas navigated by this scraper.

## About BoxOfficeMojo
Box Office Mojo has a plethora of movie information; box office charts ranging from daily to yearly performances. The database structure from which they've 
dynamically created their website makes their information very accessible to webcrawlers. 

## About IMDB.com
IMDB is a popular online database of information on movies, tv, etc. They describe themselves as "...the world's most popular and authoritative source..." for said content. 

## run.py
run.py imports the WeeklyCharts class from Scraping/boxofficeweekly.py and opens it with the syntax '''with WeeklyCharts(start=year.week, stop=year.week) as bot:'''. The crawl method is 
called and the bot begins to crawl BoxOfficeMojo weekly charts, aggregating a dictionary of movies and movieURLs. This dictionary is than transformed and concatenated onto a dataframe at the end of each page. To find the next page we use the structure of the website to alter what suffix we end the string with. (ex. the 51st week of 2020 = weekly/2020W51/) The movie list and movie URLS are saved to a csv file.

## run_movie.py
run_movie.py opens the movie url list which has been aggregated and creates a 1D dictionary.
the crawl method is called and the crawler attempts to navigate to each of the pages and collect information on:
* Budget
* MPAA Rating
* Genre
* Gross Domestic
* Gross International
* Gross Total

<h3>Issues with BoxMojo</h3>
Here two common issues would occur. The first issue would be a lack of documentation on budget and gross revenue. The second would be if the movie was a re-release it would display the amount grossed from the rerelease, not the original. Here is where we can use BoxOfficeMojo's sister site IMDB.

<h3>Finding Data Elsewhere</h3>
It is apparent that BoxOfficeMojo and IMDB use the same database. We are able to isolate each title id using the regex; re.compile('/title/.{2}\d+/') on the urlstring. We can take that string and swap the prefix out for the IMDB prefixs of https://pro.imdb.com/title/ and https://www.imdb.com/.

<p>pro.imdb.com/title is a paid service which asks you to login, however the entire page is populated with the movie's actual data instead of pseudotext. Any user would be able to just activate their scrollbar and access everything on the page.</p>
<p>However the data is also accessible on https://www.imdb.com/. Since these two sites use flex script to populate, I decided to use Selenium with a Chrome driver to allow a dynamic wait time for the page to populate. If pro.imdb.com doesn't return the data, we proceed to the non-pro imdb.com to try a second time to find Budget and rating certificates. IMDB's flex script requires Selenium to scroll down for the data to load.</p>

