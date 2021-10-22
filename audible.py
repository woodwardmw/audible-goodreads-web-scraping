from bs4 import BeautifulSoup
from webbot import Browser 

LIST_OF_ITEMS_SELECT_PREFIX = None # Input here
TEXT_DIV_SELECT_PREFIX = None
IMAGE_DIV_SELECT_PREFIX = None
df = pd.DataFrame({'Audible_Title':pd.Series([], dtype='str'), 'Audible_Subtitle':pd.Series([], dtype='str'), 'Audible_Author':pd.Series([], dtype='str'), 'Audible_Link':pd.Series([], dtype='str'), 'Image_Link':pd.Series([], dtype='str'), 'Audible_Category':pd.Series([], dtype='str'), 'Goodreads_Link':pd.Series([], dtype='str'), 'Amazon_Link':pd.Series([], dtype='str'), 'Goodreads_Rating':pd.Series([], dtype='float'), 'Number_of_Ratings':pd.Series([], dtype='int')})

class Category:
    """A category in the Audible sale"""
    url: str
    category_name: str
    def __init__(self, category_name, url):
        self.url = url
        self.category_name = category_name

class AudiblePage(Category):
    """An Audible page, corresponding to (part of) a category, with multiple books listed"""
    category: Category
    page_number: int
    def __init__(self, category, page_number):
        super().__init__(self, category.category_name, category.url)
        self.page_number = page_number
    
    def get_html_list_of_items(self, web) -> list:
        """For the Audible page, returns a list of HTML chunks each list entry containing the HTML relating to one book"""
            web.go_to(self.url + '&pageSize=50&page=' + str(self.page_number))
            audible_page_html = web.get_page_source()
            audible_page_html_parsed = BeautifulSoup(audible_page_html, 'html.parser')
            items_html_parsed = audible_page_html_parsed.select(LIST_OF_ITEMS_SELECT_PREFIX)
            return items_html_parsed

class AudibleItem(AudiblePage):
    """An Audible item, defined by a chunk of HTML, relating to one book"""
    category: Category
    html_for_item: str   # I think. But maybe it's something else, that comes from audible_page.get_html_list_of_items?
    def __init__(self, category, html_for_item):
        self.category = category
        self.title, self.subtitle, self.author, self.audible_link, self.image_link = self.get_data_from_html(html_for_item)

    def get_data_from_html(self, html_for_item):
        """Get title, author, etc from HTML for item"""
        text_div = html_for_item.select(TEXT_DIV_SELECT_PREFIX)  #[0]
        imaged_div = html_for_item.select(IMAGE_DIV_SELECT_PREFIX)[0]
        title = text_div[0].find_all('h3')[0].text.strip()
        print(title)
        try:
            subtitle = text_div[0].select('li.subtitle')[0].find_all('span')[0].text.strip()
        except:
            subtitle = ''
        author = text_div[0].select('li.authorLabel')[0].find_all('span')[0].text.replace('By:','').strip()
        audible_link = 'https://www.audible.com' + imaged_div.find_all('a')[0].get('href')
        image_link = imaged_div.find_all('img')[0].get('src').replace('_SL32_QL50_ML2_', '_SL500_')
        return title, subtitle, author, audible_link, image_link


categories_dict = {'cat1': 'url1', 'cat2': 'url2'}
categories = [Category(name = key, url = value) for key, value in categories_dict.items()]

audible_pages = [AudiblePage(category, i+1) for i, category in enumerate(categories)] # No, we need multiple pages per category, not just one per category
audible_pages_html = {}
for audible_page in audible_pages:
    audible_pages_html[audible_page] = audible_page.get_html_list_of_items(web) # This is a list for each audible_page, so a dictionary of lists

    audible_items = [AudibleItem(audible_page.category_name, html_for_item) for html_for_item in audible_pages_html[audible_page]]
    for audible_item in audible_items:
        if df['Audible_Title'].str.contains(audible_item.title, regex = False).any() == False:  # If the title is not already in the database, add it to the database
            df.loc[len(df),:] = [audible_item.title, audible_item.subtitle, audible_item.author, audible_item.audible_link, audible_item.image_link, audible_item.category, None, None, None, None]
        elif df.loc[df['Audible_Title'].str.contains(audible_item.title, regex = False)]['Audible_Category'].str.contains(audible_item.category, regex = False).any() == False:  # If it's already in the database and doesn't have the current category, add the current category
            df.loc[df.loc[:,'Audible_Title'].str.contains(audible_item.title, regex = False), 'Audible_Category'] = df.loc[df.loc[:,'Audible_Title'].str.contains(audible_item.title, regex = False), 'Audible_Category'] + ', ' + audible_item.category
        