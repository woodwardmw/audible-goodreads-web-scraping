import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import re
import utils
import math
# import requests
import aiohttp
import asyncio
import settings

def getRatingFromRow(row):
    ratingLinks = row.findAll('span', {'class': 'minirating'})
    for link in ratingLinks:
        ratingString = re.split('\s', link.text.strip())
        GRrating = float(ratingString[ratingString.index('avg')-1])
        GRnumratings = ratingString[ratingString.index('avg')+3]
        GRnumratings = int(GRnumratings.replace(",", ""))
    return GRrating, GRnumratings

def get_rating_from_url(url):
    goodreads_rating = None
    goodreads_num_ratings = None
    try:
        page = requests.get(url)
        soup = BeautifulSoup(page.text, 'html.parser')
        bookMeta = soup.select('body > div.content > div.mainContentContainer > div.mainContent > div.mainContentFloat > div.leftContainer > div#topcol > div#metacol > div#bookMeta')
        ratingSpan = bookMeta[0].findAll('span', {'itemprop': 'ratingValue'})
        goodreads_rating = re.split('\s', ratingSpan[0].text.strip())[0]
        numRatingsSpan = bookMeta[0].findAll('meta', {'itemprop': 'ratingCount'})
        goodreads_num_ratings = re.split('\s', numRatingsSpan[0].text.strip())[0]
    except:
        pass
    return goodreads_rating, goodreads_num_ratings

async def get_rating_from_search(title, author):
    goodreads_match = None
    search_url = get_search_url(title, author)
    # goodreads_page = requests.get(search_url)
    async with aiohttp.ClientSession() as session:
        async with session.get(search_url) as response:
            goodreads_page = await response.text()
            goodreads_soup = BeautifulSoup(goodreads_page, 'html.parser')
            rows = goodreads_soup.select('body > div > div > div > div > div.leftContainer > table.tableList > tr')
            possibles = get_possible_matches_from_rows(rows, title, author)
            goodreads_match = utils.best_row_item(possibles)
            print(goodreads_match)
    if goodreads_match:
        return goodreads_match.goodreads_rating, goodreads_match.goodreads_num_ratings, goodreads_match.goodreads_link
    title = re.sub(r'\[.+\]', '', title)
    author = re.sub(r', The Great Courses', '', author)
    search_url = get_search_url(title, author)
    async with aiohttp.ClientSession() as session:
        async with session.get(search_url) as response:
            goodreads_page = await response.text()
            goodreads_soup = BeautifulSoup(goodreads_page, 'html.parser')
            rows = goodreads_soup.select('body > div > div > div > div > div.leftContainer > table.tableList > tr')
            possibles = get_possible_matches_from_rows(rows, title, author)
            goodreads_match = utils.best_row_item(possibles)
            print(goodreads_match)
    if goodreads_match:
        return goodreads_match.goodreads_rating, goodreads_match.goodreads_num_ratings, goodreads_match.goodreads_link
    return None, None, None

def get_possible_matches_from_rows(rows, title, author):
    possibles = []
    for row in rows:
        titleLinks = row.findAll('a',{'class': 'bookTitle'})
        for link in titleLinks:
            goodreads_title = link.find('span').text
            goodreads_link = 'https://www.goodreads.com' + link.get('href')
        authorLinks = row.findAll('a',{'class': 'authorName'})
        for link in authorLinks:
            goodreads_author = link.find('span').text
            author_tokens = utils.get_tokens(author)
            goodreads_author_tokens = utils.get_tokens(goodreads_author)
            title_tokens = utils.get_tokens(title)
            goodreads_title_tokens = utils.get_tokens(goodreads_title)
            # print(author_tokens)
            # print(goodreads_author_tokens)
            # print(title_tokens)
            # print(goodreads_title_tokens)
            # print(utils.compare_lists(author_tokens, goodreads_author_tokens))
            # print(utils.compare_lists(title_tokens, goodreads_title_tokens))
            if utils.compare_lists(author_tokens, goodreads_author_tokens) >=min(len(goodreads_title_tokens), len(goodreads_title_tokens), 2) and utils.compare_lists(title_tokens, goodreads_title_tokens) >= min(len(title_tokens), len(title_tokens), 2):
                # print('Possible match')      
                goodreads_rating, goodreads_num_ratings = getRatingFromRow(row)
                possibles.append(GoodreadsMatch(goodreads_link, goodreads_rating, goodreads_num_ratings))
                # print(possibles)
                break
    return possibles


def get_search_url(title, author):
    title_adjusted = title.split(':', 1)[0].replace(' ', '+').replace("'","%27")
    author_adjusted = author.replace(' ', '+').replace("'","%27").replace('PhD', '').replace('MD', '').replace('Dr ', '').replace('Dr.', '').replace('translator', '').replace('foreword', '').replace('featuring', '').replace('introduction', '').replace('note', '').replace('afterword', '').replace('essay', '').replace('contributor', '')
    return 'https://www.goodreads.com/search?q=' + title_adjusted + '+' + author_adjusted

class GoodreadsMatch:
    def __init__(self, goodreads_link, goodreads_rating = None, goodreads_num_ratings = None):
        self.goodreads_link = goodreads_link
        self.goodreads_rating = goodreads_rating
        self.goodreads_num_ratings = goodreads_num_ratings

    def __repr__(self) -> str:
        return self.goodreads_link + ' ' + str(self.goodreads_rating) + ' ' + str(self.goodreads_num_ratings)

async def get_goodreads_ratings(books):
    results = await asyncio.gather(*[get_rating_from_search(book.title, book.author) for book in books])
    await asyncio.sleep(0.1)
    for i in range(len(results)):
        books[i].average_rating, books[i].num_ratings, books[i].goodreads_link = results[i]
        if not books[i].goodreads_link:
            books[i].goodreads_link = 'Failed'
    return [book for book in books]
