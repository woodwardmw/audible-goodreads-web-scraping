from bs4 import BeautifulSoup
from webbot import Browser
import pandas as pd
import time
import audible
import pickle
import json
from types import SimpleNamespace
import os
import settings



class Setup:
        
    def audibleLogin(self):
        web = Browser()
        web.go_to('https://www.amazon.com/ap/signin?clientContext=133-8565718-7694964&openid.return_to=https%3A%2F%2Fwww.audible.com%2F%3FoverrideBaseCountry%3Dtrue%26pf_rd_p%3D27448286-da3b-4d18-b236-d4299a63a797%26pf_rd_r%3DM7P9G7XTQA54YGKBZCM5%26ipRedirectOverride%3Dtrue%26%3D&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.assoc_handle=audible_shared_web_us&openid.mode=checkid_setup&marketPlaceId=AF2M0KC94RCEA&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&pageId=amzn_audible_bc_us&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0&openid.pape.max_auth_age=900&siteState=audibleid.userType%3Damzn%2Caudibleid.mode%3Did_res%2CclientContext%3D136-3313877-4249540%2CsourceUrl%3Dhttps%253A%252F%252Fwww.audible.com%252F%253FoverrideBaseCountry%25253Dtrue%252526pf_rd_p%25253D27448286-da3b-4d18-b236-d4299a63a797%252526pf_rd_r%25253DM7P9G7XTQA54YGKBZCM5%252526ipRedirectOverride%25253Dtrue%252526%2Csignature%3DosFxeuOwWVQcTSj2BceMSdDy7d4wYj3D&pf_rd_p=00c37833-8fd7-4332-bdb1-cd84f72c7953&pf_rd_r=GKJWN891WPPXKXCSBXXE') 
        time.sleep(10)
        return web

    def getCategories(self, web, CATEGORY_SELECT, BASE_URL):
        categories = []
        web.go_to(BASE_URL)
        page = web.get_page_source()
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
        print(categories)
        self.saveJson(categories, 'categories.json')
        self.saveBin(categories, 'categories.bin')
    
    def loadCategories(self, source = 'bin'):
        if source == 'bin':
            categories = self.loadBin('categories.bin')
        else:
            if 'web' not in locals():
                web = self.audibleLogin()
            categories = self.getCategories(web, settings.CATEGORY_SELECT, settings.BASE_URL)
        return categories

    def saveBooks(self, books):
        print(books)
        self.saveJson(books, 'books.json')
        self.saveBin(books, 'books.bin')
    
    def loadBooks(self, source = 'bin'):
        if source == 'bin':
            books = self.loadBin('books.bin')
        else:
            if not categories:
                raise ValueError("Need to provide categories or source from file")
            for category in categories:
                if 'web' not in locals():
                    web = self.audibleLogin()
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

def main():
    setup = Setup()
    categories = setup.loadCategories('bin')
    print(categories)

if __name__ == '__main__':
    main()