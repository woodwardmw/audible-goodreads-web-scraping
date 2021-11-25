IMPORT_CATEGORIES_SOURCE = 'bin'  # 'bin' or 'web'
IMPORT_BOOKS_SOURCE = 'bin' # 'bin' or 'web'
# GET_AUDIBLE_DATA = True
GET_GOODREADS_RATINGS = True
GET_AMAZON_LINKS = False
REFRESH_EXISTING = True

BASE_URL = 'https://www.audible.com/ep/black-friday-week-sale-2021'
#BASE_CATEGORY = 'fiction'
CATEGORY_SELECT = 'body > div.adbl-page > div.adbl-main > div#center-5 > div.bc-row-responsive > div.bc-col-responsive > div.bc-box > div.bc-box-padding-mini > div.bc-container > div.bc-row-responsive'
BOOK_ITEM_SELECT = 'body > div.adbl-page > div.adbl-main > div#center-10 > div.bc-section > div > span > ul > div > li.productListItem'  # to end in li
IMAGE_DIV_SELECT = 'div.bc-row-responsive > div.bc-col-9 > div.bc-row-responsive > div.bc-col-4 > div.bc-row-responsive > div.bc-col-12 > div'
TEXT_DIV_SELECT = 'div.bc-row-responsive > div.bc-col-9 > div.bc-row-responsive > div.bc-col-7 > div.bc-row-responsive > div.bc-col-12 > span > ul'

BOOK_FILE = 'Black_Friday_Sale_Nov_2021.csv'  # Can be just the Audible list, or an already processed merge of Audible and Goodreads Data
LINKED_URLS = 'Linked_URLs.csv'


