from bs4 import BeautifulSoup
from webbot import Browser
import pandas as pd
import time
import audible
import pickle
import json

df = pd.DataFrame({'Audible_Title':pd.Series([], dtype='str'), 'Audible_Subtitle':pd.Series([], dtype='str'), 'Audible_Author':pd.Series([], dtype='str'), 'Audible_Link':pd.Series([], dtype='str'), 'Image_Link':pd.Series([], dtype='str'), 'Audible_Category':pd.Series([], dtype='str'), 'Goodreads_Link':pd.Series([], dtype='str'), 'Amazon_Link':pd.Series([], dtype='str'), 'Goodreads_Rating':pd.Series([], dtype='float'), 'Number_of_Ratings':pd.Series([], dtype='int')})

class Setup:
        
    def audibleLogin():
        web = Browser()
        web.go_to('https://www.amazon.com/ap/signin?clientContext=133-8565718-7694964&openid.return_to=https%3A%2F%2Fwww.audible.com%2F%3FoverrideBaseCountry%3Dtrue%26pf_rd_p%3D27448286-da3b-4d18-b236-d4299a63a797%26pf_rd_r%3DM7P9G7XTQA54YGKBZCM5%26ipRedirectOverride%3Dtrue%26%3D&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.assoc_handle=audible_shared_web_us&openid.mode=checkid_setup&marketPlaceId=AF2M0KC94RCEA&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&pageId=amzn_audible_bc_us&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0&openid.pape.max_auth_age=900&siteState=audibleid.userType%3Damzn%2Caudibleid.mode%3Did_res%2CclientContext%3D136-3313877-4249540%2CsourceUrl%3Dhttps%253A%252F%252Fwww.audible.com%252F%253FoverrideBaseCountry%25253Dtrue%252526pf_rd_p%25253D27448286-da3b-4d18-b236-d4299a63a797%252526pf_rd_r%25253DM7P9G7XTQA54YGKBZCM5%252526ipRedirectOverride%25253Dtrue%252526%2Csignature%3DosFxeuOwWVQcTSj2BceMSdDy7d4wYj3D&pf_rd_p=00c37833-8fd7-4332-bdb1-cd84f72c7953&pf_rd_r=GKJWN891WPPXKXCSBXXE') 
        time.sleep(10)
        return web

    def getCategories(web, CATEGORY_SELECT, BASE_URL):
        categories = []
        web.go_to(BASE_URL)
        page = web.get_page_source()
        soup = BeautifulSoup(page, 'html.parser')
        
        info = soup.select(CATEGORY_SELECT)
        # print(info)
        for part in info:
            links = part.findAll('a')
            # print(links)
            for link in links:
                # print("Here")
                if link.text != 'All Categories':
                    categories.append(audible.Category(link.text, 'https://www.audible.com' + link.get('href').split('&')[0]))
        return categories

    def createBook(audibleItem):
        return audible.Book(audibleItem.title, audibleItem.author, audibleItem.audible_link, audibleItem.image_link, audibleItem.category_name, subtitle = audibleItem.subtitle)

    def saveBin(variable, filename):
        with open(filename, 'wb') as file:
            pickle.dump(variable, file, protocol=pickle.HIGHEST_PROTOCOL)

    def loadBin(filename):
        with open(filename, 'rb') as f:
            variable = pickle.load(f)
            return variable

    def saveJson(variable, filename):
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(variable, f, ensure_ascii=False, indent=4, default=lambda obj: obj.__dict__)

    def loadJson(filename):
        with open(filename, 'r') as f:
            variable = f.read()
        return json.loads(variable)