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

def amazonLogin():
    web = Browser()
    web.go_to('https://www.amazon.com/ap/signin?openid.pape.max_auth_age=0&openid.return_to=https%3A%2F%2Fwww.amazon.com%2F%3Fref_%3Dnav_signin&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.assoc_handle=usflex&openid.mode=checkid_setup&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0&') 
    time.sleep(10)
    return web

# book_file = 'Eureka Sale Sept 2021.csv'
# book_df = pd.read_csv(os.getcwd() + '/' + book_file)
# linked_URLs = pd.read_csv(os.getcwd() + '/Linked_URLs.csv')


def getAmazonMatches(book_df, linked_URLs, web, refresh_existing = False):
    for index, item in book_df.iterrows():
        if index >= 400:
            print(index)
            title = item['Audible_Title']
            print(title)
            author =  item['Audible_Author'].replace('The Great Courses', '')
            amazon_URL = ''
            print(item['Amazon_Link'])
            if ((linked_URLs['Audible_Title'] == title) & (linked_URLs['Audible_Author'] == author)).any():
                amazon_URL = linked_URLs[(linked_URLs['Audible_Title'] == title) & (linked_URLs['Audible_Author'] == author)].iloc[0]['Amazon_Link']
                print('In Linked URLs')
            else: # Get from Amazon search
                search_url = 'https://www.amazon.com/s?k=' + title.replace(' ', '+').replace("'","-") + '+' + author.replace(' ', '+').replace('PhD', '').replace('MD', '').replace('Dr', '').replace('translator', '').replace('foreword', '').replace('featuring', '').replace('introduction', '').replace('note', '').replace('afterword', '') + '&i=audible'
                web.go_to(search_url)
                page = web.get_page_source()
                soup = BeautifulSoup(page, 'html.parser')
                if len(soup.select('body > div#a-page > div#search > div.s-desktop-content > div.sg-col > div.sg-col-inner > span > div.s-result-list > div > div.sg-col-inner > span > div > div > div.sg-row > div.sg-col-8-of-16 > div.sg-col-inner > div.a-section > div.a-section > h2')) > 0:
                    amazon_URL = soup.select('body > div#a-page > div#search > div.s-desktop-content > div.sg-col > div.sg-col-inner > span > div.s-result-list > div > div.sg-col-inner > span > div > div > div.sg-row > div.sg-col-8-of-16 > div.sg-col-inner > div.a-section > div.a-section > h2')[0].find_all('a')[0].get('href')
                    print(amazon_URL)
                    amazon_URL = 'https://www.amazon.com' + amazon_URL + '&tag=listenerslist-20'
            book_df.loc[index,'Amazon_Link'] = amazon_URL
    return book_df

