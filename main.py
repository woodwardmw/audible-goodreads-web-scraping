import getData
import audible
import goodreads
import pandas as pd
import os

BOOK_FILE = 'Black_Friday_Sale_Nov_2021.csv'  # Can be just the Audible list, or an already processed merge of Audible and Goodreads Data
LINKED_URLS = 'Linked_URLs.csv'
df = pd.DataFrame({'Audible_Title':pd.Series([], dtype='str'), 'Audible_Subtitle':pd.Series([], dtype='str'), 'Audible_Author':pd.Series([], dtype='str'), 'Audible_Link':pd.Series([], dtype='str'), 'Image_Link':pd.Series([], dtype='str'), 'Audible_Category':pd.Series([], dtype='str'), 'Goodreads_Link':pd.Series([], dtype='str'), 'Amazon_Link':pd.Series([], dtype='str'), 'Goodreads_Rating':pd.Series([], dtype='float'), 'Number_of_Ratings':pd.Series([], dtype='int')})

IMPORT_CATEGORIES_FROM_FILE = 'Bin'  # Importing from Json is difficult, trying to get the Json data back into custom objects. It's easier to import from Bin.
IMPORT_BOOKS_FROM_FILE = 'Bin'
GET_AUDIBLE_DATA = True
GET_GOODREADS_RATINGS = True
GET_AMAZON_LINKS = False
REFRESH_EXISTING = False

BASE_URL = 'https://www.audible.com/ep/black-friday-week-sale-2021'
#BASE_CATEGORY = 'fiction'
CATEGORY_SELECT = 'body > div.adbl-page > div.adbl-main > div#center-5 > div.bc-row-responsive > div.bc-col-responsive > div.bc-box > div.bc-box-padding-mini > div.bc-container > div.bc-row-responsive'
BOOK_ITEM_SELECT = 'body > div.adbl-page > div.adbl-main > div#center-10 > div.bc-section > div > span > ul > div > li.productListItem'  # to end in li
IMAGE_DIV_SELECT = 'div.bc-row-responsive > div.bc-col-9 > div.bc-row-responsive > div.bc-col-4 > div.bc-row-responsive > div.bc-col-12 > div'
TEXT_DIV_SELECT = 'div.bc-row-responsive > div.bc-col-9 > div.bc-row-responsive > div.bc-col-7 > div.bc-row-responsive > div.bc-col-12 > span > ul'

linked_URLs = pd.read_csv(os.getcwd() + '/Linked_URLs.csv')

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
    setup.saveBin(categories, 'categories.bin')


    if IMPORT_BOOKS_FROM_FILE == 'Bin':
        books = setup.loadBin('books_full_data.bin')
    elif IMPORT_BOOKS_FROM_FILE == 'Json':
        books = setup.loadJson('books_full_data.json')
    else:
        for category in categories:
            if 'web' not in locals():
                web = setup.audibleLogin()
            print(f'Category type is {type(category)}')
            category.pages = category.getAudiblePages(web)
        books = []
        for category in categories:
            if hasattr(category, 'pages'):
                for page in category.pages:
                    if hasattr(page, 'items'):
                        for item in page.items:
                            books.append(audible.Book(item.title, item.author, item.audible_link, item.image_link, item.category_name, subtitle = item.subtitle))
        setup.saveJson(books, 'books_full_data.json')
        setup.saveBin(books, 'books_full_data.bin')


    if GET_GOODREADS_RATINGS:
        for book in books:
            print(f'Title: {book.title}, Author: {book.author}')
            if book.is_in_df(linked_URLs):
                book.goodreads_link = book.get_df_field(linked_URLs, 'Goodreads_Link')
                book.average_rating, book.num_ratings = goodreads.get_rating_from_url(book.goodreads_link)
            else:
                book.average_rating, book.num_ratings = goodreads.get_rating_from_search(book.title, book.author)
        setup.saveJson(books, 'books_full_data.json')
        setup.saveBin(books, 'books_full_data.bin')

    for book in books:
        if book.is_in_df(df):
            book.add_category(book.category_list, df)
        else:
            book.add_to_df(df)

if __name__ == "__main__":
    main()