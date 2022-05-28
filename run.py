from Scraping.boxofficeweekly import WeeklyCharts

# bot = WeeklyCharts(2020.01, 2022.15)
# bot.crawl()
# bot.save_final_df()
# bot.save_movie_urls()
with WeeklyCharts(start=2020.01, stop=2022.15) as bot:
    bot.crawl()
    bot.save_final_df()
    bot.save_movie_urls()
