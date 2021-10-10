
import requests
from bs4 import BeautifulSoup
from webbot import Browser 
import pandas as pd
import re
import difflib
import os
import time

def audibleLogin():
    web = Browser()
    web.go_to('https://www.amazon.com/ap/signin?clientContext=133-8565718-7694964&openid.return_to=https%3A%2F%2Fwww.audible.com%2F%3FoverrideBaseCountry%3Dtrue%26pf_rd_p%3D27448286-da3b-4d18-b236-d4299a63a797%26pf_rd_r%3DM7P9G7XTQA54YGKBZCM5%26ipRedirectOverride%3Dtrue%26%3D&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.assoc_handle=audible_shared_web_us&openid.mode=checkid_setup&marketPlaceId=AF2M0KC94RCEA&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&pageId=amzn_audible_bc_us&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0&openid.pape.max_auth_age=900&siteState=audibleid.userType%3Damzn%2Caudibleid.mode%3Did_res%2CclientContext%3D136-3313877-4249540%2CsourceUrl%3Dhttps%253A%252F%252Fwww.audible.com%252F%253FoverrideBaseCountry%25253Dtrue%252526pf_rd_p%25253D27448286-da3b-4d18-b236-d4299a63a797%252526pf_rd_r%25253DM7P9G7XTQA54YGKBZCM5%252526ipRedirectOverride%25253Dtrue%252526%2Csignature%3DosFxeuOwWVQcTSj2BceMSdDy7d4wYj3D&pf_rd_p=00c37833-8fd7-4332-bdb1-cd84f72c7953&pf_rd_r=GKJWN891WPPXKXCSBXXE') 
    time.sleep(10)
    return web
                       
def getAudibleDataForCategory(url, category, max_pages, df, web, bookItemSelect, imageDivSelect, textDivSelect1):
    page_number = 1
    while page_number <= max_pages:
        web.go_to(url + '&pageSize=50&page=' + str(page_number))
        ADpage = web.get_page_source()
        ADsoup = BeautifulSoup(ADpage, 'html.parser')
        items = ADsoup.select(bookItemSelect)
        # f = open("test2.txt", "w")  THIS CAN HELP TO VIEW THE HTML OF AN ITEM
        # f.writelines(str(items[1]))
        # f.close()
        for item in items:
            textdiv = item.select(textDivSelect1)  #[0]
            imagediv = item.select(imageDivSelect)[0]
            info = textdiv  #.select('div > div > span > ul')
            title = info[0].find_all('h3')[0].text.strip()
            print(title)
            try:
                subtitle = info[0].select('li.subtitle')[0].find_all('span')[0].text.strip()
            except:
                subtitle = ''
            author = info[0].select('li.authorLabel')[0].find_all('span')[0].text.replace('By:','').strip()
            audible_link = 'https://www.audible.com' + imagediv.find_all('a')[0].get('href')
            image_link = imagediv.find_all('img')[0].get('src').replace('_SL32_QL50_ML2_', '_SL500_')
            if df['Audible_Title'].str.contains(title).any() == False:  # If the title is not already in the database
                # print(f'Title not in database yet: {title}')    
                row = [title, subtitle, author, audible_link, image_link, category, None, None, None, None]
                # print(row)
                df.loc[len(df),:] = row
            elif df.loc[df['Audible_Title'].str.contains(title)]['Audible_Category'].str.contains(category).any() == False:
                print(df.loc[df['Audible_Title'].str.contains(title)]['Audible_Category'])
                print(f'Title: {title}')
                print(f'Category: {category}')
                df.loc[df.loc[:,'Audible_Title'].str.contains(title), 'Audible_Category'] = df.loc[df.loc[:,'Audible_Title'].str.contains(title), 'Audible_Category'] + ', ' + category
                print(df.loc[df.loc[:,'Audible_Title'].str.contains(title), 'Audible_Category'] )
        page_number += 1
    # print(df)
    return df


def getCategories(base_category, base_url, web, select):
    categories = {base_category: base_url}
    web.go_to(base_url)
    page = web.get_page_source()
    soup = BeautifulSoup(page, 'html.parser')
    
    info = soup.select(select)
    for part in info:
        links = part.findAll('a')
        for link in links:
            if link.text != 'All Categories':
                categories[link.text] = 'https://www.audible.com' + link.get('href')
    return categories

