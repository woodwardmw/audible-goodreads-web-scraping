from bs4 import BeautifulSoup
from webbot import Browser 

LIST_OF_ITEMS_SELECT_PREFIX = None # Input here

class Category:
    url: str
    category_name: str
    def __init__(self, category_name, url):
        self.url = url
        self.category_name = category_name

class AudiblePage(Category):
    category: Category
    page_number: int
    def __init__(self, category, page_number):
        super().__init__(self, category.category_name, category.url)
        self.page_number = page_number
    
    def get_html_list_of_items(self, web) -> list:
            web.go_to(self.url + '&pageSize=50&page=' + str(self.page_number))
            audible_page_html = web.get_page_source()
            audible_page_html_parsed = BeautifulSoup(audible_page_html, 'html.parser')
            items_html_parsed = audible_page_html_parsed.select(LIST_OF_ITEMS_SELECT_PREFIX)
            return items_html_parsed

class AudibleItem(AudiblePage):
    category: Category
    html_for_item: str   # I think. But maybe it's something else, that comes from audible_page.get_html_list_of_items?
    def __init__(self, category, html_for_item):
        self.category = category
        self.title, self.author = get_data_from_html(html_for_item)

        def get_data_from_html(self, html_for_item):
            """Get title, author, etc from HTML for item"""


categories_dict = {'cat1': 'url1', 'cat2': 'url2'}
categories = [Category(name = key, url = value) for key, value in categories_dict.items()]

audible_pages = [AudiblePage(category, i+1) for i, category in enumerate(categories)] # No, we need multiple pages per category, not just one per category
audible_pages_html = {}
for audible_page in audible_pages:
    audible_pages_html[audible_page] = audible_page.get_html_list_of_items(web) # This is a list for each audible_page, so a dictionary of lists

    audible_items = [AudibleItem(audible_page.category_name, html_for_item) for html_for_item in audible_pages_html[audible_page]]