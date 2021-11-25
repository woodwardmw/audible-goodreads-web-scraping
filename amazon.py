import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import re
import difflib
import math
from webbot import Browser
import time
import numpy as np
import settings



# book_file = 'Eureka Sale Sept 2021.csv'
# book_df = pd.read_csv(os.getcwd() + '/' + book_file)
# linked_URLs = pd.read_csv(os.getcwd() + '/Linked_URLs.csv')


def getAmazonMatches(books, web, refresh_existing=False):
    linked_URLs = pd.read_csv(os.getcwd() + '/data/' + settings.LINKED_URLS)
    for book in books:
        print(book)
        amazon_link = None
        search_url = 'https://www.amazon.com/s?k=' + book.title.replace(' ', '+').replace("'", "-") + '+' + book.author.replace(' ', '+').replace('PhD', '').replace('MD', '').replace(
            'Dr', '').replace('translator', '').replace('foreword', '').replace('featuring', '').replace('introduction', '').replace('note', '').replace('afterword', '') + '&i=audible'
        web.go_to(search_url)
        page = web.get_page_source()
        soup = BeautifulSoup(page, 'html.parser')
        htmlItemSnippetList = soup.select(
            'body > div#a-page > div#search > div.s-desktop-content > div.sg-col > div.sg-col-inner > span > div.s-result-list > div.s-result-item > div.sg-col-inner > span > div > div.a-section > div > div.sg-col > div.sg-col-inner > div.a-section > div.a-section > h2')
        if len(htmlItemSnippetList) > 0:
            # print(htmlItemSnippetList[0].find_all('a'))
            amazon_link = htmlItemSnippetList[0].find_all('a')[0].get('href')
            print(amazon_link)
            amazon_link = 'https://www.amazon.com' + amazon_link + '&tag=listenerslist-20'
            book.amazon_link = amazon_link
    return books

            
    # for index, item in book_df.iterrows():
    #     if True:
    #         print(index)
    #         title = item['Audible_Title']
    #         print(title)
    #         author = item['Audible_Author'].replace('The Great Courses', '')
    #         amazon_link = ''
    #         print(item['Amazon_Link'])
    #         if ((linked_URLs['Audible_Title'] == title) & (linked_URLs['Audible_Author'] == author)).any():
    #             amazon_link = linked_URLs[(linked_URLs['Audible_Title'] == title) & (
    #                 linked_URLs['Audible_Author'] == author)].iloc[0]['Amazon_Link']
    #             print('In Linked URLs')
    #         else:  # Get from Amazon search
    #             search_url = 'https://www.amazon.com/s?k=' + title.replace(' ', '+').replace("'", "-") + '+' + author.replace(' ', '+').replace('PhD', '').replace('MD', '').replace(
    #                 'Dr', '').replace('translator', '').replace('foreword', '').replace('featuring', '').replace('introduction', '').replace('note', '').replace('afterword', '') + '&i=audible'
    #             web.go_to(search_url)
    #             page = web.get_page_source()
    #             soup = BeautifulSoup(page, 'html.parser')
    #             htmlItemSnippetList = soup.select(
    #                 'body > div#a-page > div#search > div.s-desktop-content > div.sg-col > div.sg-col-inner > span > div.s-result-list > div.s-result-item > div.sg-col-inner > div > div > div > div.sg-row > div.sg-col-8-of-16 > div.sg-col-inner > div.a-section > div.a-section > h2')
    #             # print(htmlItemSnippetList)
    #             if len(htmlItemSnippetList) > 0:
    #                 print(htmlItemSnippetList[0].find_all('a'))
    #                 amazon_link = htmlItemSnippetList[0].find_all('a')[
    #                     0].get('href')
    #                 print(amazon_link)
    #                 amazon_link = 'https://www.amazon.com' + amazon_link + '&tag=listenerslist-20'
    #         book_df.loc[index, 'Amazon_Link'] = amazon_link
    # return book_df
