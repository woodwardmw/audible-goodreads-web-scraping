#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep  8 18:54:59 2021

@author: mark
"""

from numpy.core.numeric import False_
import pandas as pd
import os

from goodreads import getRating, getRatingFromRow, getGoodreadsMatches
from audible import getCategories, getAudibleDataForCategory
from amazon import amazonLogin, getAmazonMatches
from getData import audibleLogin
import audible

base_url = 'https://www.audible.com/special-promo/2for1/cat?node=23435846011'
book_file = 'Monster_Sale_Oct_2021.csv'  # Can be just the Audible list, or an already processed merge of Audible and Goodreads Data

getAudibleData = False
getGoodreadsRatings = True
getAmazonLinks = False
refresh_existing = False

categorySelect = 'body > div.adbl-page > div.adbl-main > div.bc-container > div.bc-row-responsive > div.bc-col-3 > div#left-1 > form > div > span > ul'
bookItemSelect = 'body > div.adbl-page > div.adbl-main > div.bc-container > div.bc-row-responsive > div.bc-col-9 > div#center-3 > div.bc-section > div > span > ul > div > li.productListItem'  # to end in li
imageDivSelect = 'div.bc-row-responsive > div.bc-col-8 > div.bc-row-responsive > div.bc-col-5 > div.bc-row-responsive > div.bc-col-12 > div'
textDivSelect1 = 'div.bc-row-responsive > div.bc-col-6 > div.bc-row-responsive > div.bc-col-12 > span > ul'
MAX_PAGES = 7



if getAudibleData == True:
    web = audibleLogin()
    categories = getCategories('All Titles', base_url, web, categorySelect)
    book_df = pd.DataFrame({'Audible_Title':pd.Series([], dtype='str'), 'Audible_Subtitle':pd.Series([], dtype='str'), 'Audible_Author':pd.Series([], dtype='str'), 'Audible_Link':pd.Series([], dtype='str'), 'Image_Link':pd.Series([], dtype='str'), 'Audible_Category':pd.Series([], dtype='str'), 'Goodreads_Link':pd.Series([], dtype='str'), 'Amazon_Link':pd.Series([], dtype='str'), 'Goodreads_Rating':pd.Series([], dtype='float'), 'Number_of_Ratings':pd.Series([], dtype='int')})
    for _, (category, audibleurl) in enumerate(categories.items()):  # I think this could be  for category, audibleurl in categories.items():
        if category != 'All Titles':
            print(f'Category: {category}')
            book_df = getAudibleDataForCategory(audibleurl, category, MAX_PAGES, book_df, web, bookItemSelect, imageDivSelect, textDivSelect1)

    # Need to remove duplicates (by title and author) as these mess up the goodreads matching
    book_df.to_csv(os.getcwd() + '/' + book_file)



if getGoodreadsRatings == True:
    linked_URLs = pd.read_csv(os.getcwd() + '/Linked_URLs.csv')
    book_df = pd.read_csv(os.getcwd() + '/' + book_file)
    goodreads_df = getGoodreadsMatches(book_df, linked_URLs, refresh_existing)
    book_df.update(goodreads_df)    
    book_df.to_csv(os.getcwd() + '/' + book_file, index = False)


if getAmazonLinks == True:
    linked_URLs = pd.read_csv(os.getcwd() + '/Linked_URLs.csv')
    book_df = pd.read_csv(os.getcwd() + '/' + book_file)
    web=amazonLogin()
    getAmazonMatches(book_df, linked_URLs, web, refresh_existing = False)
    book_df.to_csv(os.getcwd() + '/' + book_file, index = False)


# book_df = pd.read_csv(os.getcwd() + '/' + book_file)
# book_df = book_df.astype({'Amazon_Link': str})




book_df.to_csv(os.getcwd() + '/' + book_file, index = False)




