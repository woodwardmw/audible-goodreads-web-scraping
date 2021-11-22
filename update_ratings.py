
import pandas as pd
import requests
import os
from bs4 import BeautifulSoup
import re

book_file = 'Goodreads Ratings 2-for-1 Sept 2021 List.csv'
book_df = pd.read_csv(os.getcwd() + '/' + book_file)

linked_URLs = pd.read_csv(os.getcwd() + '/Linked_URLs.csv')

# linked_URLs.dropna(subset = ['Goodreads_Link'], axis = 0, inplace = True)
# linked_URLs[['Audible_Title', 'Audible_Author', 'Goodreads_Link']].to_csv(os.getcwd() + '/Linked_URLs.csv')

# linked_URLs = pd.read_csv(os.getcwd() + '/Linked_URLs.csv')


# for index, item in book_df.iterrows():
#     title = item['Audible_Title']
#     author = item['Audible_Author']
#     mask = (linked_URLs['Audible_Title'] == title) & (linked_URLs['Audible_Author'] == author)

#     rating, numRatings = getRating()


def getRating(url):
    GRrating = None
    GRnumratings = None
    try:
        page = requests.get(url)
        soup = BeautifulSoup(page.text, 'html.parser')
        bookMeta = soup.select('body > div.content > div.mainContentContainer > div.mainContent > div.mainContentFloat > div.leftContainer > div#topcol > div#metacol > div#bookMeta')
        ratingSpan = bookMeta[0].findAll('span', {'itemprop': 'ratingValue'})
        GRrating = re.split('\s', ratingSpan[0].text.strip())[0]
        numRatingsSpan = bookMeta[0].findAll('meta', {'itemprop': 'ratingCount'})
        GRnumratings = re.split('\s', numRatingsSpan[0].text.strip())[0]
    except:
        pass
    return GRrating, GRnumratings
