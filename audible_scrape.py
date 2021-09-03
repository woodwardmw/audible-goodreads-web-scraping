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
                                                                                                    
def getAudibleData(url, category, max_pages):
    df = pd.DataFrame({'Audible Title':pd.Series([], dtype='str'), 'Audible Subtitle':pd.Series([], dtype='str'), 'Audible Author':pd.Series([], dtype='str'), 'Audible Link':pd.Series([], dtype='str'), 'Image Link':pd.Series([], dtype='str'), 'Audible Category':pd.Series([], dtype='str')})
    page_number = 1
    while page_number <= max_pages:
        web.go_to(url + '&pageSize=50&page=' + str(page_number))
        ADpage = web.get_page_source()
        ADsoup = BeautifulSoup(ADpage, 'html.parser')
        items = ADsoup.select('body > div > div > div#center-8 > div > div > span > ul > div > li')
        # f = open("test2.txt", "w")  THIS CAN HELP TO VIEW THE HTML OF AN ITEM
        # f.writelines(str(items[1]))
        # f.close()
        for item in items:
            textdiv = item.select('div > div > div > div.bc-col-7')[0]
            imagediv = item.select('div > div > div > div.bc-col-4 > div > div > div')[0]
            info = textdiv.select('div > span > ul')
            title = info[0].find_all('h3')[0].text.strip()
            try:
                subtitle = info[0].select('li.subtitle')[0].find_all('span')[0].text.strip()
            except:
                subtitle = ''
            author = info[0].select('li.authorLabel')[0].find_all('span')[0].text.replace('By:','').strip()
            audible_link = imagediv.find_all('a')[0].get('href')
            image_link = imagediv.find_all('img')[0].get('src').replace('_SL32_QL50_ML2_', '_SL500_')
        if df['Audible Title'].str.contains(title).any() == False:  # If the title is not already in the database
            row = [title, subtitle, author, audible_link, image_link, category]
            df.loc[len(df),:] = row
        elif df.loc[df['Audible Title'].str.contains(title)]['Audible Category'].str.contains(category).any() == False:
            print(df.loc[df['Audible Title'].str.contains(title)]['Audible Category'])
            print(f'Title: {title}')
            print(f'Category: {category}')
            df.loc[df.loc[:,'Audible Title'].str.contains(title), 'Audible Category'] = df.loc[df.loc[:,'Audible Title'].str.contains(title), 'Audible Category'] + ', ' + category
            print(df.loc[df.loc[:,'Audible Title'].str.contains(title), 'Audible Category'] )
        page_number += 1
    return df

def getRating(row):
    ratingLinks = row.findAll('span', {'class': 'minirating'})
    for link in ratingLinks:
        # print(link)
        ratingString = re.split('\s', link.text.strip())
        print(ratingString)
        GRrating = ratingString[ratingString.index('avg')-1]
        # print(GRrating)
        GRnumratings = ratingString[ratingString.index('avg')+3]
    return GRrating, GRnumratings


def getGoodreadsMatches(audible_df):
    possibles = pd.DataFrame({'Book ID':pd.Series([], dtype='int'),'Goodreads Title':[], 'Goodreads Author':[], 'Goodreads Link':[], 'Goodreads Rating':pd.Series([], dtype='float'), 'Number of Ratings':pd.Series([], dtype='int')})
    for index, row in audible_df.iterrows():
        title = row['Audible Title']
        author =  row['Audible Author']
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
                    GRlink = 'https://www.goodreads.com' + link.get('href')
                    print('Goodreads title is: ' + GRtitle)
                authorLinks = row.findAll('a',{'class': 'authorName'})
                for link in authorLinks:
                    GRauthor = link.find('span').text
                    # print('Goodreads author is: ' + GRauthor)
                    # print("Goodreads title word: " + ascii(re.sub(r'[^\w\s]','',GRtitle.split()[0])))
                    # print("Audible title word: " + ascii(re.sub(r'[^\w\s]','',title.split()[0])))
                    # word1 = re.sub(r'[^\w\s]','',GRauthor.split()[0])
                    # word2 = re.sub(r'[^\w\s]','',author.split()[0])
                    # print(word1 == word2)
                    # print(re.sub(r'[^\w\s]','',GRauthor.split()[0]) == re.sub(r'[^\w\s]','',author.split()[0]))
                    #print(re.sub(r'[^\w\s]','',author.replace("'", "")).split()[0])
                    if len(re.sub(r'[^\w\s]','',author.replace("'", "")).split()) > 1:
                        if re.sub(r'[^\w\s]','',author.replace("'", "")).split()[1] in re.sub(r'[^\w\s]','',GRauthor.replace("'", "")).split() and re.sub(r'[^\w\s]','',GRtitle.replace("'", "")).split()[0] == re.sub(r'[^\w\s]','',title.replace("'", "")).split()[0]:
                            #print('GR Title matches: ' + GRtitle)
                            # print('Set rating')
                            GRrating, GRnumratings = getRating(row)
                            possibleRow = [index, GRtitle, GRauthor, GRlink, float(GRrating), int(GRnumratings.replace(',', ''))]
                            possibles.loc[len(possibles)] = possibleRow
                            break
                    else:     
                        if re.sub(r'[^\w\s]','',author.replace("'", "")).split()[0] in re.sub(r'[^\w\s]','',GRauthor.replace("'", "")).split() and re.sub(r'[^\w\s]','',GRtitle.replace("'", "")).split()[0] == re.sub(r'[^\w\s]','',title.replace("'", "")).split()[0]:
                            # print('GR Title matches: ' + GRtitle)
                            # print('Set rating')
                            GRrating, GRnumratings = getRating(row)
                            possibleRow = [index, GRtitle, GRauthor, GRlink, float(GRrating), int(GRnumratings.replace(',', ''))]
                            possibles.loc[len(possibles)] = possibleRow
                            break
      
    idx = possibles.groupby(['Book ID'])['Number of Ratings'].transform(max) == possibles['Number of Ratings']
    GRdf = possibles[idx]
    return GRdf

base_url = 'https://www.audible.com/ep/the-great-courses-scimath?pageSize=50&ref=a_ep_the-gr_c8_pageSize_3&pf_rd_p=9f7cde6d-e2dc-42f2-b9bf-a6ed6be0b5e2&pf_rd_r=YS8CPMX8DZYCMDPVBGVH'

def getCategories(base_category, base_url):
    categories = {base_category: base_url}
    web.go_to(base_url)
    page = web.get_page_source()
    soup = BeautifulSoup(page, 'html.parser')
    
    info = soup.select('body > div > div > div#center-6 > div > div > div > div > div > div > div')
    for part in info:
        links = part.findAll('a')
        for link in links:
            if link.text != 'Featured':
                categories[link.text] = 'https://www.audible.com' + link.get('href')
    return categories

categories = getCategories('Science & Math', 'https://www.audible.com/ep/the-great-courses-scimath?pf_rd_p=9f7cde6d-e2dc-42f2-b9bf-a6ed6be0b5e2&pf_rd_r=YS8CPMX8DZYCMDPVBGVH')
df = pd.DataFrame({'Audible Title':pd.Series([], dtype='str'), 'Audible Subtitle':pd.Series([], dtype='str'), 'Audible Author':pd.Series([], dtype='str'), 'Audible Link':pd.Series([], dtype='str'), 'Image Link':pd.Series([], dtype='str'), 'Audible Category':pd.Series([], dtype='str')})
max_pages = 4

for _, (category, audibleurl) in enumerate(categories.items()):
    df.append(getAudibleData(audibleurl, category, max_pages), ignore_index = True)

goodreads_df = getGoodreadsMatches(df)



new = df.merge(goodreads_df, left_index = True, right_on = 'Book ID', how = 'left')
new.to_csv('ratings.csv')

