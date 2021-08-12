#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 10 17:29:58 2021

@author: mark
"""

import requests
from bs4 import BeautifulSoup
from webbot import Browser 
import pandas as pd
import re
import difflib
web = Browser()
web.go_to('https://www.amazon.com/ap/signin?clientContext=133-8565718-7694964&openid.return_to=https%3A%2F%2Fwww.audible.com%2F%3FoverrideBaseCountry%3Dtrue%26pf_rd_p%3D27448286-da3b-4d18-b236-d4299a63a797%26pf_rd_r%3DM7P9G7XTQA54YGKBZCM5%26ipRedirectOverride%3Dtrue%26%3D&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.assoc_handle=audible_shared_web_us&openid.mode=checkid_setup&marketPlaceId=AF2M0KC94RCEA&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&pageId=amzn_audible_bc_us&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0&openid.pape.max_auth_age=900&siteState=audibleid.userType%3Damzn%2Caudibleid.mode%3Did_res%2CclientContext%3D136-3313877-4249540%2CsourceUrl%3Dhttps%253A%252F%252Fwww.audible.com%252F%253FoverrideBaseCountry%25253Dtrue%252526pf_rd_p%25253D27448286-da3b-4d18-b236-d4299a63a797%252526pf_rd_r%25253DM7P9G7XTQA54YGKBZCM5%252526ipRedirectOverride%25253Dtrue%252526%2Csignature%3DosFxeuOwWVQcTSj2BceMSdDy7d4wYj3D&pf_rd_p=00c37833-8fd7-4332-bdb1-cd84f72c7953&pf_rd_r=GKJWN891WPPXKXCSBXXE') 


df = pd.DataFrame({'Audible Title':[], 'Audible Subtitle':[], 'Audible Author':[]})
max_pages = 2
page_number = 1
while page_number <= max_pages:
    if page_number == 1:
        ADurl = "https://www.audible.com/special-promo/2for1/cat?node=23568839011&pageSize=50"
    else:
        ADurl = "https://www.audible.com/special-promo/2for1/cat?node=23568839011&pageSize=50&page=" + str(page_number)
    web.go_to(ADurl)
    ADpage = web.get_page_source()
    ADsoup = BeautifulSoup(ADpage, 'html.parser')
    
    ADinfo = ADsoup.select('body > div > div > div > div > div > div#center-3 > div > div > span > ul > div > li.bc-list-item > div > div > div > div > div > div > span > ul')
    
    for part in ADinfo:
        h3_title = part.select('h3')
        #for titleSelection in h3_title:
        title = h3_title[0].find('a').contents[0]
        span_subtitle = part.select('li.subtitle')
        if len(span_subtitle) > 0 :
            subtitle = span_subtitle[0].find('span').contents[0]
        else:
            subtitle = None
        span_author = part.select('li.authorLabel > span')
        if len(span_author) > 0 :
            author = span_author[0].find('a').contents[0]
        row = [title, subtitle, author]
        df.loc[len(df)] = row
    page_number += 1


possibles = pd.DataFrame({'Book ID':pd.Series([], dtype='int'),'Goodreads Title':[], 'Goodreads Author':[], 'Goodreads Rating':pd.Series([], dtype='float'), 'Number of Ratings':pd.Series([], dtype='int')})
for index, row in df.iterrows():
    title = row['Audible Title']
    author =  row['Audible Author']
    GRratings = []
    GRurl = 'https://www.goodreads.com/search?q=' + title.replace(' ', '+').replace("'","-") + '+' + author.replace(' ', '+').replace('PhD', '').replace('MD', '')
    #print(url)
    if True:  # Can be modified to restrict to a certain index
        print('Audible title is: ' + title)
        print('Audible author is: ' + author)
        print(GRurl)
        GRpage = requests.get(GRurl)
        GRsoup = BeautifulSoup(GRpage.text, 'html.parser')
        rows = GRsoup.select('body > div > div > div > div > div.leftContainer > table.tableList > tr')
        for row in rows:
            titleLinks = row.findAll('a',{'class': 'bookTitle'})
            for link in titleLinks:
                GRtitle = link.find('span').text
                print('Goodreads title is: ' + GRtitle)
            authorLinks = row.findAll('a',{'class': 'authorName'})
            for link in authorLinks:
                GRauthor = link.find('span').text
                print('Goodreads author is: ' + GRauthor)
                print("Goodreads title word: " + ascii(re.sub(r'[^\w\s]','',GRtitle.split()[0])))
                print("Audible title word: " + ascii(re.sub(r'[^\w\s]','',title.split()[0])))
                word1 = re.sub(r'[^\w\s]','',GRauthor.split()[0])
                word2 = re.sub(r'[^\w\s]','',author.split()[0])
                print(word1 == word2)
                print(re.sub(r'[^\w\s]','',GRauthor.split()[0]) == re.sub(r'[^\w\s]','',author.split()[0]))
                if re.sub(r'[^\w\s]','',GRauthor.replace("'", "").split()[0]) == re.sub(r'[^\w\s]','',author.replace("'", "").split()[0]) and re.sub(r'[^\w\s]','',GRtitle.replace("'", "").split()[0]) == re.sub(r'[^\w\s]','',title.replace("'", "").split()[0]):
                    print('GR Title matches: ' + GRtitle)
                    print('Set rating')
                    ratingLinks = row.findAll('span', {'class': 'minirating'})
                    for link in ratingLinks:
                        # print(link)
                        ratingString = re.split('\s', link.text.strip())
                        print(ratingString)
                        GRrating = ratingString[ratingString.index('avg')-1]
                        # print(GRrating)
                        GRnumratings = ratingString[ratingString.index('avg')+3]
                    possibleRow = [index, GRtitle, GRauthor, float(GRrating), int(GRnumratings.replace(',', ''))]
                    possibles.loc[len(possibles)] = possibleRow
  
idx = possibles.groupby(['Book ID'])['Number of Ratings'].transform(max) == possibles['Number of Ratings']
GRdf = possibles[idx]

def getRating(row):
    

new = df.merge(GRdf, left_index = True, right_on = 'Book ID', how = 'left')
new.to_csv('ratings.csv')

