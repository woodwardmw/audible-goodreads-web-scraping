from bs4 import BeautifulSoup
from webbot import Browser
import pandas as pd
import time
import audible
import amazon
import pickle
import json
from types import SimpleNamespace
import os
import settings
from selenium import webdriver



class Setup:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        
    def audibleLogin(self):
        web = webdriver.Chrome("chromedriver")
        web.get('https://www.amazon.com/ap/signin?clientContext=133-8565718-7694964&openid.return_to=https%3A%2F%2Fwww.audible.com%2F%3FoverrideBaseCountry%3Dtrue%26pf_rd_p%3D27448286-da3b-4d18-b236-d4299a63a797%26pf_rd_r%3DM7P9G7XTQA54YGKBZCM5%26ipRedirectOverride%3Dtrue%26%3D&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.assoc_handle=audible_shared_web_us&openid.mode=checkid_setup&marketPlaceId=AF2M0KC94RCEA&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&pageId=amzn_audible_bc_us&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0&openid.pape.max_auth_age=900&siteState=audibleid.userType%3Damzn%2Caudibleid.mode%3Did_res%2CclientContext%3D136-3313877-4249540%2CsourceUrl%3Dhttps%253A%252F%252Fwww.audible.com%252F%253FoverrideBaseCountry%25253Dtrue%252526pf_rd_p%25253D27448286-da3b-4d18-b236-d4299a63a797%252526pf_rd_r%25253DM7P9G7XTQA54YGKBZCM5%252526ipRedirectOverride%25253Dtrue%252526%2Csignature%3DosFxeuOwWVQcTSj2BceMSdDy7d4wYj3D&pf_rd_p=00c37833-8fd7-4332-bdb1-cd84f72c7953&pf_rd_r=GKJWN891WPPXKXCSBXXE') 
        web.find_element('name', 'email').send_keys(self.username)
        web.find_element('name', 'password').send_keys(self.password)
        web.find_element("id", "signInSubmit").click()
        return web
        
    
    def amazonLogin(self):
        web = Browser()
        web.go_to('https://www.amazon.com/ap/signin?openid.pape.max_auth_age=0&openid.return_to=https%3A%2F%2Fwww.amazon.com%2F%3Fref_%3Dnav_signin&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.assoc_handle=usflex&openid.mode=checkid_setup&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0&')
        time.sleep(10)
        return web

    def getCategories(self, web, CATEGORY_SELECT, BASE_URL):
        categories = []
        web.get(BASE_URL)
        page = web.page_source
        soup = BeautifulSoup(page, 'html.parser')
        
        info = soup.select(CATEGORY_SELECT)
        for part in info:
            links = part.findAll('a')
            for link in links:
                if link.text != 'All Categories':
                    categories.append(audible.Category(link.text, 'https://www.audible.com' + link.get('href').split('&')[0]))
        return categories

    def createBook(self, audibleItem):
        return audible.Book(audibleItem.title, audibleItem.author, audibleItem.audible_link, audibleItem.image_link, audibleItem.category_name, subtitle = audibleItem.subtitle)

    def saveBin(self, variable, filename):
        with open(filename, 'wb') as file:
            pickle.dump(variable, file, protocol=pickle.HIGHEST_PROTOCOL)

    def loadBin(self, filename):
        with open(filename, 'rb') as f:
            variable = pickle.load(f)
            return variable

    def saveJson(self, variable, filename):
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(variable, f, ensure_ascii=False, indent=4, default=lambda obj: obj.__dict__)

    def loadJson(self, filename):
        with open(filename, 'r') as f:
            variable = f.read()

        return json.loads(variable, object_hook=lambda d: SimpleNamespace(**d))

    def saveCategories(self, categories):
        print(f'Saving {len(categories)} categories to file')
        # print(categories)
        self.saveJson(categories, 'categories.json')
        self.saveBin(categories, 'categories.bin')
    
    def loadCategories(self, source = 'bin'):
        if source == 'bin':
            print('Loading categories from file')
            categories = self.loadBin('categories.bin')
        else:
            if 'web' not in locals():
                web = self.audibleLogin()
            print('Scraping categories from audible.com')
            categories = self.getCategories(web, settings.CATEGORY_SELECT, settings.BASE_URL)
        return categories

    def saveBooks(self, books):
        # print(books)
        print(f'Saving {len(books)} books')
        self.saveJson(books, 'books.json')
        self.saveBin(books, 'books.bin')
    
    def loadBooks(self, source = 'bin', categories = None):
        if source == 'bin':
            print('Loading books from file')
            books = self.loadBin('books.bin')
            print(f'{len(books)} books loaded')
        else:
            if not categories:
                raise ValueError("Need to provide categories or source from file")
            for category in categories:
                if 'web' not in locals():
                    web = self.audibleLogin()
                print('Scraping books from audible.com')
                category.pages = category.getAudiblePages(web)
            books = []
            for category in categories:
                if hasattr(category, 'pages'):
                    for page in category.pages:
                        if hasattr(page, 'items'):
                            for item in page.items:
                                book = audible.Book(item.title, item.author, item.audible_link, item.image_link, item.category_name, subtitle = item.subtitle)
                                print(book)
                                books.append(book)
        return books
    
    def getAmazonLinks(self, books):
        if 'web' not in locals():
                web = self.amazonLogin()
        print('Scraping Amazon links from amazon.com')
        books = amazon.getAmazonMatches(books, web)
        return books

def main():
    setup = Setup()
    categories = setup.loadCategories('bin')
    print(categories)

if __name__ == '__main__':
    main()