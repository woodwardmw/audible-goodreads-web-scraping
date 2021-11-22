import getData
import pickle
import json
import audible
from goodreads import getRating

BOOK_FILE = 'Black_Friday_Sale_Nov_2021.csv'  # Can be just the Audible list, or an already processed merge of Audible and Goodreads Data

IMPORT_CATEGORIES_FROM_FILE = False
IMPORT_BOOKS_FROM_FILE = False
GET_AUDIBLE_DATA = True
GET_GOODREADS_RATINGS = False
GET_AMAZON_LINKS = False
REFRESH_EXISTING = False

BASE_URL = 'https://www.audible.com/ep/black-friday-week-sale-2021'
#BASE_CATEGORY = 'fiction'
CATEGORY_SELECT = 'body > div.adbl-page > div.adbl-main > div#center-5 > div.bc-row-responsive > div.bc-col-responsive > div.bc-box > div.bc-box-padding-mini > div.bc-container > div.bc-row-responsive'
BOOK_ITEM_SELECT = 'body > div.adbl-page > div.adbl-main > div#center-10 > div.bc-section > div > span > ul > div > li.productListItem'  # to end in li
IMAGE_DIV_SELECT = 'div.bc-row-responsive > div.bc-col-9 > div.bc-row-responsive > div.bc-col-4 > div.bc-row-responsive > div.bc-col-12 > div'
TEXT_DIV_SELECT = 'div.bc-row-responsive > div.bc-col-9 > div.bc-row-responsive > div.bc-col-7 > div.bc-row-responsive > div.bc-col-12 > span > ul'

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