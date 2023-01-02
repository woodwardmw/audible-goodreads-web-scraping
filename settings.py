IMPORT_CATEGORIES_SOURCE = "bin"  # 'bin' or 'web'
IMPORT_BOOKS_SOURCE = "bin"  # 'bin' or 'web'
# GET_AUDIBLE_DATA = True
GET_GOODREADS_RATINGS = True
GET_AMAZON_LINKS = False
REFRESH_EXISTING = True

BASE_URL = "https://www.audible.com/special-promo/2for1/cat?node=23435846011"
# BASE_CATEGORY = 'fiction'
CATEGORY_SELECT = "body > div.adbl-page > div.adbl-main > div.bc-container > div.bc-row-responsive > div.bc-col-responsive > div#left-1 > form > div.categories > span > ul.bc-list"  # > div.bc-box-padding-mini > div.bc-container > div.bc-row-responsive'
BOOK_ITEM_SELECT = "body > div.adbl-page > div.adbl-main > div.bc-container > div.bc-row-responsive > div.bc-col-responsive > div#center-3 > div.bc-section > div.adbl-impression-container > div > span > ul.bc-list > li.productListItem"  # to end in li
IMAGE_DIV_SELECT = "div.bc-row-responsive > div.bc-col-8 > div.bc-row-responsive > div.bc-col-5 > div.bc-row-responsive > div.bc-col-12 > div"
TEXT_DIV_SELECT = "div.bc-row-responsive > div.bc-col-8 > div.bc-row-responsive > div.bc-col-6 > div.bc-row-responsive > div.bc-col-12 > span > ul"

BOOK_FILE = "Dec-2022-Two-for-One.csv"  # Can be just the Audible list, or an already processed merge of Audible and Goodreads Data
LINKED_URLS = "Linked_URLs.csv"
