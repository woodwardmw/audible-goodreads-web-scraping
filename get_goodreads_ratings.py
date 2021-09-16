#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep  8 18:54:59 2021

@author: mark
"""

import pandas as pd
import os
import re
from pandas.core.base import SelectionMixin
import requests
from bs4 import BeautifulSoup
import math
from goodreads import getRating, getRatingFromRow, getGoodreadsMatches
from audible import audibleLogin, getCategories, getAudibleDataForCategory
from amazon import amazonLogin, getAmazonMatches

base_url = 'https://www.audible.com/ep/eureka-sale?ref=a_ep_eureka_c5_tab1&pf_rd_p=418e7020-0b96-4cbc-919e-79c851f139ff&pf_rd_r=8BHDCJ5N7RHGQF8F4ZNF'
book_file = 'Eureka Sale Sept 2021.csv'  # Can be just the Audible list, or an already processed merge of Audible and Goodreads Data

# web = audibleLogin()
# categorySelect = 'body > div.adbl-page > div.adbl-main > div#center-5 > div > div > div.bc-box > div.bc-color-secondary > div.bc-container > div.bc-spacing-mini > div.bc-col-responsive'

# categories = getCategories('All Titles', base_url, web, categorySelect)
# book_df = pd.DataFrame({'Audible_Title':pd.Series([], dtype='str'), 'Audible_Subtitle':pd.Series([], dtype='str'), 'Audible_Author':pd.Series([], dtype='str'), 'Audible_Link':pd.Series([], dtype='str'), 'Image_Link':pd.Series([], dtype='str'), 'Audible_Category':pd.Series([], dtype='str'), 'Goodreads_Link':pd.Series([], dtype='str'), 'Amazon_Link':pd.Series([], dtype='str'), 'Goodreads_Rating':pd.Series([], dtype='float'), 'Number_of_Ratings':pd.Series([], dtype='int')})
# book_df = pd.read_csv(os.getcwd() + '/' + book_file)
# max_pages = 5
# bookItemSelect = 'body > div.adbl-page > div.adbl-main > div#center-10 > div > div > span > ul > div.adbl-impression-container > li.productListItem'  # to end in li
# imageDivSelect = 'div > div.bc-col-9 > div > div.bc-col-4 > div > div.bc-col-12 > div'
# textDivSelect1 = 'div > div.bc-col-9 > div > div.bc-col-7 > div > div.bc-col-12 > span > ul'


# for _, (category, audibleurl) in enumerate(categories.items()):
#     if category != 'All Titles':
#         book_df = getAudibleDataForCategory(audibleurl, category, max_pages, book_df, web, bookItemSelect, imageDivSelect, textDivSelect1)

# Need to remove duplicates (by title and author) as these mess up the goodreads matching


# book_df.to_csv(os.getcwd() + '/' + book_file)

web=amazonLogin()

book_df = pd.read_csv(os.getcwd() + '/' + book_file)
book_df = book_df.astype({'Amazon_Link': str})
linked_URLs = pd.read_csv(os.getcwd() + '/Linked_URLs.csv')

# goodreads_df = getGoodreadsMatches(book_df, linked_URLs, refresh_existing = False)
# print(goodreads_df.head(20))
# book_df.update(goodreads_df)
book_df = getAmazonMatches(book_df, linked_URLs, web)


book_df.to_csv(os.getcwd() + '/' + book_file, index = False)




