import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import re
import utils

def getRatingFromRow(row):
    ratingLinks = row.findAll('span', {'class': 'minirating'})
    for link in ratingLinks:
        # print(link)
        ratingString = re.split('\s', link.text.strip())
        print(ratingString)
        GRrating = ratingString[ratingString.index('avg')-1]
        # print(GRrating)
        GRnumratings = ratingString[ratingString.index('avg')+3]
    return GRrating, GRnumratings

def get_rating_from_url(url):
    goodreads_rating = None
    goodreads_num_ratings = None
    try:
        page = requests.get(url)
        soup = BeautifulSoup(page.text, 'html.parser')
        bookMeta = soup.select('body > div.content > div.mainContentContainer > div.mainContent > div.mainContentFloat > div.leftContainer > div#topcol > div#metacol > div#bookMeta')
        ratingSpan = bookMeta[0].findAll('span', {'itemprop': 'ratingValue'})
        goodreads_rating = re.split('\s', ratingSpan[0].text.strip())[0]
        numRatingsSpan = bookMeta[0].findAll('meta', {'itemprop': 'ratingCount'})
        goodreads_num_ratings = re.split('\s', numRatingsSpan[0].text.strip())[0]
    except:
        pass
    return goodreads_rating, goodreads_num_ratings

def get_rating_from_search(title, author):
    goodreads_match = None
    title_adjusted = title.split(':', 1)[0].replace(' ', '+').replace("'","%27")
    author_adjusted = author.replace(' ', '+').replace("'","%27").replace('PhD', '').replace('MD', '').replace('Dr', '').replace('translator', '').replace('foreword', '').replace('featuring', '').replace('introduction', '').replace('note', '').replace('afterword', '').replace('essay', '').replace('contributor', '')
    search_url = 'https://www.goodreads.com/search?q=' + title_adjusted + '+' + author_adjusted
    goodreads_page = requests.get(search_url)
    goodreads_soup = BeautifulSoup(goodreads_page.text, 'html.parser')
    rows = goodreads_soup.select('body > div > div > div > div > div.leftContainer > table.tableList > tr')
    for row in rows:
        possibles = []
        titleLinks = row.findAll('a',{'class': 'bookTitle'})
        for link in titleLinks:
            goodreads_title = link.find('span').text
            goodreads_link = 'https://www.goodreads.com' + link.get('href')
            print('Goodreads title is: ' + goodreads_title)
        authorLinks = row.findAll('a',{'class': 'authorName'})
        for link in authorLinks:
            goodreads_author = link.find('span').text
        author_tokens = utils.get_tokens(author)
        goodreads_author_tokens = utils.get_tokens(goodreads_author)
        title_tokens = utils.get_tokens(title)
        goodreads_title_tokens = utils.get_tokens(goodreads_title)
        if utils.compare_lists(author_tokens, goodreads_author_tokens) >=2 and utils.compare_lists(title_tokens, goodreads_title_tokens) >=2:      
            goodreads_rating, goodreads_num_ratings = getRatingFromRow(row)
            possibles.append(GoodreadsMatch(goodreads_link, goodreads_rating, goodreads_num_ratings)) 
            finished = True
            break
        goodreads_match = utils.best_row_item(possibles)
    if goodreads_match:
        return goodreads_match.goodreads_rating, goodreads_match.goodreads_num_ratings
    return None, None

class GoodreadsMatch:
    def __init__(self, goodreads_link, goodreads_rating = None, goodreads_num_ratings = None):
        self.goodreads_link = goodreads_link
        self.goodreads_rating = goodreads_rating
        self.goodreads_num_ratings = goodreads_num_ratings

# def getGoodreadsMatches(book_df, linked_URLs, refresh_existing = False):
#     possibles = pd.DataFrame({'Book ID':pd.Series([], dtype='int'), 'Goodreads_Link':[], 'Goodreads_Rating':pd.Series([], dtype='float'), 'Number_of_Ratings':pd.Series([], dtype='int')})
#     for index, item in book_df.iterrows():
#         finished = False
#         if True:

#             title = item['Audible_Title']
#             print(title)
#             author =  item['Audible_Author'].replace('The Great Courses', '')
#             print(author)
#             if refresh_existing == False:
#                 print(f'Goodreads Rating: {item["Goodreads_Rating"]}')
#                 if math.isnan(item['Goodreads_Rating']) == False and item['Goodreads_Rating'] > 0:
#                     possibleRow = [index, item['Goodreads_Link'], item['Goodreads_Rating'], item['Number_of_Ratings']]
#                     possibles.loc[len(possibles)] = possibleRow
#                     finished = True
#                     continue

#             if ((linked_URLs['Audible_Title'] == title) & (linked_URLs['Audible_Author'] == author)).any(): # Get from linked_URLs, then goodreads
#                 goodreads_URL = linked_URLs[(linked_URLs['Audible_Title'] == title) & (linked_URLs['Audible_Author'] == author)].iloc[0]['Goodreads_Link']
#                 print(f'Goodreads URL: {goodreads_URL}')
#                 GRrating, GRnumratings = getRating(goodreads_URL)
#                 print(f'{GRrating}, {GRnumratings}')
#                 if GRnumratings is not None:
#                     possibleRow = [index, goodreads_URL, float(GRrating), int(GRnumratings.replace(',', ''))]
#                     possibles.loc[len(possibles)] = possibleRow
#                     finished = True
#             else: # Get from Goodreads search
#                 title = title.split(':', 1)[0]
#                 search_url = 'https://www.goodreads.com/search?q=' + title.replace(' ', '+').replace("'","%27") + '+' + author.replace(' ', '+').replace("'","%27").replace('PhD', '').replace('MD', '').replace('Dr', '').replace('translator', '').replace('foreword', '').replace('featuring', '').replace('introduction', '').replace('note', '').replace('afterword', '').replace('essay', '').replace('contributor', '')
#                 if True:  # Can be modified to restrict to a certain index
#                     GRpage = requests.get(search_url)
#                     GRsoup = BeautifulSoup(GRpage.text, 'html.parser')
#                     rows = GRsoup.select('body > div > div > div > div > div.leftContainer > table.tableList > tr')
#                     for row in rows:
#                         titleLinks = row.findAll('a',{'class': 'bookTitle'})
#                         for link in titleLinks:
#                             GRtitle = link.find('span').text
#                             GRlink = 'https://www.goodreads.com' + link.get('href')
#                             print('Goodreads title is: ' + GRtitle)
#                         authorLinks = row.findAll('a',{'class': 'authorName'})
#                         for link in authorLinks:
#                             GRauthor = link.find('span').text
#                             if len(re.sub(r'[^\w\s]','',author.replace("'", "")).split()) > 1:
#                                 if re.sub(r'[^\w\s]','',author.replace("'", "")).split()[1] in re.sub(r'[^\w\s]','',GRauthor.replace("'", "%27s")).split() and re.sub(r'[^\w\s]','',GRtitle.replace("'", "")).split()[0] == re.sub(r'[^\w\s]','',title.replace("'", "")).split()[0]:
#                                     GRrating, GRnumratings = getRatingFromRow(row)
#                                     possibleRow = [index, GRlink, float(GRrating), int(GRnumratings.replace(',', ''))]
#                                     possibles.loc[len(possibles)] = possibleRow
#                                     finished = True
#                                     break
#                                 elif re.sub(r'[^\w\s]','',author.replace("'", "")).split()[-1] in re.sub(r'[^\w\s]','',GRauthor.replace("'", "")).split() and re.sub(r'[^\w\s]','',GRtitle.replace("'", "")).split()[0] == re.sub(r'[^\w\s]','',title.replace("'", "")).split()[0]:
#                                     GRrating, GRnumratings = getRatingFromRow(row)
#                                     possibleRow = [index, GRlink, float(GRrating), int(GRnumratings.replace(',', ''))]
#                                     possibles.loc[len(possibles)] = possibleRow
#                                     finished = True
#                                     break
#                             elif len(re.sub(r'[^\w\s]','',author.replace("'", "")).split()) > 0:     
#                                 if re.sub(r'[^\w\s]','',author.replace("'", "")).split()[0] in re.sub(r'[^\w\s]','',GRauthor.replace("'", "")).split() and re.sub(r'[^\w\s]','',GRtitle.replace("'", "")).split()[0] == re.sub(r'[^\w\s]','',title.replace("'", "")).split()[0]:
#                                     GRrating, GRnumratings = getRatingFromRow(row)
#                                     possibleRow = [index, GRlink, float(GRrating), int(GRnumratings.replace(',', ''))]
#                                     possibles.loc[len(possibles)] = possibleRow
#                                     finished = True
#                                     break
#                             elif re.sub(r'[^\w\s]','',GRtitle.replace("'", "")).split()[0] == re.sub(r'[^\w\s]','',title.replace("'", "")).split()[0]:
#                                 GRrating, GRnumratings = getRatingFromRow(row)
#                                 possibleRow = [index, GRlink, float(GRrating), int(GRnumratings.replace(',', ''))]
#                                 possibles.loc[len(possibles)] = possibleRow
#                                 finished = True
#                                 break
#         if finished == False:
#             possibleRow = [index, '', 0, 0]
#             possibles.loc[len(possibles)] = possibleRow

#     # idx = possibles.groupby(['Book ID'])['Number_of_Ratings'].transform(max) == possibles['Number_of_Ratings']
#     # GRdf = possibles[idx].reset_index(drop=True)
#     GRdf = possibles.loc[possibles.groupby('Book ID')['Number_of_Ratings'].idxmax()].reset_index(drop=True)
#     return GRdf

# # df = pd.read_csv(os.getcwd() + '/Audible 2-for-1 Sept 2021 List.csv')
# # goodreads_df = getGoodreadsMatches(df)

# # new = df.merge(goodreads_df, left_index = True, right_on = 'Book ID', how = 'left')
# # new.to_csv(os.getcwd() + '/Goodreads Ratings 2-for-1 Sept 2021.csv')
