from scraping.indeed import job_filtration
import scraping.constants as const

with job_filtration() as bot:
    bot.open_site(const.url)
    bot.top_movies()
    data= bot.top_movies_list()
    bot.save_to_files(data)