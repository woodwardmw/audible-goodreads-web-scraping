from bs4 import BeautifulSoup
import json
import re
import requests
import pandas as pd


from main import BOOK_ITEM_SELECT, IMAGE_DIV_SELECT, TEXT_DIV_SELECT

class Category:
    """A category in the Audible sale"""
    def __init__(self, category_name, url):
        self.url = url
        assert re.match('^http[s]*:\/\/', self.url), 'The URL must start with http(s)://'
        self.category_name = category_name
    
    # def __repr__(self):
    #     return self.category_name + ': ' + self.url
    
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)

    def getAudiblePages(self, web, START_PAGE = 1):
        audible_pages = []
        page_number = START_PAGE
        assert isinstance(page_number, int) and page_number >= 1 
        while True:
            new_page = AudiblePage(self.category_name, self.url, page_number, web)
            print(new_page)
            if not audible_pages:
                audible_pages.append(new_page)
                print(f'Page {page_number} added')
            elif new_page == audible_pages[-1]:
                print(f'Page {page_number} is the same as the previous one')
                break
            else:
                audible_pages.append(new_page)
                print(f'Page {page_number} added')
            page_number += 1
        return audible_pages

    def __repr__(self):
        return self.category_name + ': ' + self.url

    # def toJSON(self):
    #     return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

class AudiblePage:
    """An Audible page, corresponding to (part of) a category, with multiple books listed"""
    category: Category
    page_number: int

    def __init__(self, category_name, category_url, page_number, web):
        self.category_name = category_name
        self.category_url = category_url
        self.page_number = page_number
        self.html_list_of_items = self.get_html_list_of_items(web, BOOK_ITEM_SELECT)
        self.items = self.getAudibleItems(IMAGE_DIV_SELECT, TEXT_DIV_SELECT)

    # def __repr__(self):
    #     return self.category_name + ' / Page ' + str(self.page_number)
    
    def get_html_list_of_items(self, web, BOOK_ITEM_SELECT) -> list:
        """For the Audible page, returns a list of HTML chunks, each list entry containing the HTML relating to one book"""
        web.go_to(self.category_url + '&pageSize=50&page=' + str(self.page_number))
        audible_page_html = web.get_page_source()
        audible_page_html_parsed = BeautifulSoup(audible_page_html, 'html.parser')
        html_list_of_items = audible_page_html_parsed.select(BOOK_ITEM_SELECT)
        return html_list_of_items

    def getAudibleItems(self, IMAGE_DIV_SELECT, TEXT_DIV_SELECT) -> list:
        audible_items = []
        for html_for_item in self.html_list_of_items:
            new_item = AudibleItem(self.category_name, html_for_item, IMAGE_DIV_SELECT, TEXT_DIV_SELECT)
            print(new_item)
            if any(item.title == new_item.title and item.author == new_item.author for item in audible_items):
                existing_item = next(item for item in audible_items if item.title == new_item.title and item.author == new_item.author)
                existing_item.category_name = existing_item.category_name + ', ' + self.category_name
            else:
                audible_items.append(new_item)
        return audible_items
    
    def __eq__(self, other):
        if isinstance(other, AudiblePage) and self.html_list_of_items is not None:
            return self.items[0].title == other.items[0].title and self.items[0].author == other.items[0].author
    
    def __repr__(self):
        return self.category_name + ': Page ' + str(self.page_number)

class AudibleItem:
    """An Audible item, defined by a chunk of HTML, relating to one book"""
    category: Category
    html_for_item: str   # I think. But maybe it's something else, that comes from audible_page.get_html_list_of_items?
    def __init__(self, category_name, html_for_item, IMAGE_DIV_SELECT, TEXT_DIV_SELECT):
        self.category_name = category_name
        self.text_div = html_for_item.select(TEXT_DIV_SELECT)  #[0]
        self.image_div = html_for_item.select(IMAGE_DIV_SELECT)[0]
        self.title = self.get_title()
        self.subtitle = self.get_subtitle()
        self.author = self.get_author()
        self.audible_link = self.get_audible_link()
        self.image_link = self.get_image_link()
    
    def __eq__(self, other):
        if isinstance(other, AudibleItem):
            return self.title == other.title and self.author == other.author

    # def __repr__(self):
    #     if self.author:
    #         return self.title + ', ' + self.author
    #     else:
    #         return self.title

    def get_title(self):
        """Get title for the item"""
        title = self.text_div[0].find_all('h3')[0].text.strip()
        return title

    def get_subtitle(self):
        """Get subtitle (if any) for the item"""
        try:
            subtitle = self.text_div[0].select('li.subtitle')[0].find_all('span')[0].text.strip()
        except:
            subtitle = None
        return subtitle

    def get_author(self):
        """Get author for the item"""
        try:
            author = self.text_div[0].select('li.authorLabel')[0].find_all('span')[0].text.replace('By:','').strip()
        except:
            author = None
        else:
            return author
    
    def get_audible_link(self):
        """Get Audible Link for the item"""
        audible_link = 'https://www.audible.com' + self.image_div.find_all('a')[0].get('href')
        return audible_link
    
    def get_image_link(self):
        """Get Audible Image Link for the item"""
        image_link = self.image_div.find_all('img')[0].get('src').replace('_SL32_QL50_ML2_', '_SL500_')
        return image_link
    
    def __repr__(self):
        if self.author:
            return self.title + ': ' + self.author
        else:
            return self.title

class Book:
    def __init__(self, title, author, audible_link, image_link, category_list, subtitle = None, goodreads_link = None, amazon_link = None, average_rating = 0, num_ratings = 0):
        self.title = title
        # assert self.title is None or isinstance(self.title, str)
        self.subtitle = subtitle
        # assert self.subtitle is None or isinstance(self.subtitle, str)
        self.author = author
        # assert self.author is None or isinstance(self.author, str)
        self.audible_link = audible_link
        # assert self.audible_link is None or isinstance(self.audible_link, str)
        self.image_link = image_link
        # assert self.image_link is None or isinstance(self.image_link, str)
        self.category_list = category_list
        # assert self.category_name is None or isinstance(self.category_name, str)
        self.goodreads_link = goodreads_link
        # assert self.goodreads_link is None or isinstance(self.goodreads_link, str)
        self.amazon_link = amazon_link
        # assert self.amazon_link is None or isinstance(self.amazon_link, str)
        self.average_rating = average_rating
        # assert self.average_rating is None or isinstance(self.category_name, float)
        self.num_ratings = num_ratings
        # assert self.num_ratings is None or isinstance(self.num_ratings, int)
    


    def already_in_df(self, df):
        if row_in_df := df['Audible_Title'].str.contains(self.title, regex = False).any():  # If the title matches a title of a row in the df, check whether the author matches the author of that row in the df
            # row_in_df = df['Audible_Title'].str.contains(self.title, regex = False)
            return df.loc[row_in_df]['Audible_Author'].str.contains(self.author, regex = False) # Previously had .any() - maybe it needs that?
        else:
            return False
    
    def add_to_df(self, df):
        """Add this book to the df"""
        df.loc[len(df),:] = [self.title, self.subtitle, self.author, self.audible_link, self.image_link, ', '.join(self.category_list), self.goodreads_link, self.amazon_link, self.average_rating, self.num_ratings]

    def add_category(self, category_name, df):
        # self.category_list.append(category_name)
        if df['Audible_Title'].str.contains(self.title, regex = False).any():
            row_in_df = df.index[df['Audible_Title'].str.contains(self.title, regex = False)]
            df.loc[row_in_df, 'Audible_Category'] += ', ' + category_name
            print(f'Categories in df: {df.loc[row_in_df]["Audible_Category"]}')

    
    # def get_goodreads_rating(self):

    def is_in_df(self, df):
        if ((df['Audible_Title'] == self.title) & (df['Audible_Author'] == self.author)).any(): # Get from df, then goodreads
            return True
        return False
    
    def get_df_field(self, df, field):
        return df[(df['Audible_Title'] == self.title) & (df['Audible_Author'] == self.author)].iloc[0][field]
    
    
    
    # if GRnumratings is not None:
    #     possibleRow = [index, goodreads_URL, float(GRrating), int(GRnumratings.replace(',', ''))]
    #     possibles.loc[len(possibles)] = possibleRow
    #     finished = True

    


    def __repr__(self):
        if self.author:
            return self.title + ': ' + self.author + '\n' + str(self.category_list)
        else:
            return self.title + '\n' + str(self.category_list)



    
