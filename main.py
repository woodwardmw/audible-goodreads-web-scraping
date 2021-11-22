import getData
import pickle
import json
import audible

BOOK_FILE = 'Monster_Sale_Oct_2021.csv'  # Can be just the Audible list, or an already processed merge of Audible and Goodreads Data

IMPORT_CATEGORIES_FROM_FILE = 'Json'
IMPORT_BOOKS_FROM_FILE = 'Json'
GET_AUDIBLE_DATA = False
GET_GOODREADS_RATINGS = True
GET_AMAZON_LINKS = False
REFRESH_EXISTING = False

BASE_URL = 'https://www.audible.com/search?node=18573518011'
#BASE_CATEGORY = 'fiction'
CATEGORY_SELECT = 'body > div.adbl-page > div.adbl-main > div.bc-container > div.bc-row-responsive > div.bc-col-3 > div#left-1 > form > div > div > span > ul'
BOOK_ITEM_SELECT = 'body > div.adbl-page > div.adbl-main > div.bc-container > div.bc-row-responsive > div.bc-col-9 > div#center-3 > div.bc-section > div > span > ul > div > li.productListItem'  # to end in li
IMAGE_DIV_SELECT = 'div.bc-row-responsive > div.bc-col-8 > div.bc-row-responsive > div.bc-col-5 > div.bc-row-responsive > div.bc-col-12 > div'
TEXT_DIV_SELECT = 'div.bc-row-responsive > div.bc-col-8 > div.bc-row-responsive > div.bc-col-6 > div.bc-row-responsive > div.bc-col-12 > span > ul'

def obj_dict(obj):
    return obj._asdict()



def main():
    setup = getData.Setup
    if IMPORT_CATEGORIES_FROM_FILE == 'Bin':
        categories = setup.loadBin('categories.bin')
    elif IMPORT_CATEGORIES_FROM_FILE == 'Json':
        categories = setup.loadJson('categories.json')
    else:
        if 'web' not in locals():
            web = setup.audibleLogin()
        categories = setup.getCategories(web, CATEGORY_SELECT, BASE_URL)

    print(categories)
    setup.saveJson(categories, 'categories.json')

    if IMPORT_BOOKS_FROM_FILE == 'Bin':
        books = setup.loadBin('books_full_data.bin')
    elif IMPORT_BOOKS_FROM_FILE == 'Json':
        books = setup.loadJson('books_full_data.json')
    else:
        for category in categories:
            if 'web' not in locals():
                web = setup.audibleLogin()
            category.pages = category.getAudiblePages(web)
        books = []
        for category in categories:
            if hasattr(category, 'pages'):
                for page in category.pages:
                    if hasattr(page, 'items'):
                        for item in page.items:
                            books.append(audible.Book(item.title, item.author, item.audible_link, item.image_link, item.category_name, subtitle = item.subtitle))
        setup.saveJson(books, 'books_full_data.json')
    print(books)
    setup.saveJson(books, 'books_full_data.json')

if __name__ == "__main__":
    main()