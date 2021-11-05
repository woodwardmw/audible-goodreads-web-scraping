import pandas as pd
import os

book_file = 'Vital Listens Sale Oct 2021.csv'
linked_URLs = pd.read_csv(os.getcwd() + '/' + 'Linked_URLs.csv')
book_df = pd.read_csv(os.getcwd() + '/' + book_file)

def add_new_linked_urls(linked_URLs, book_database):
    book_database.dropna(axis = 0, subset = ['Goodreads_Link'], inplace = True)

    for index, item in book_database.iterrows():
        if True:
            print(f'Index: {index}')
            title = item['Audible_Title']
            # print(title)
            author = item['Audible_Author']
            # print(author)
            goodreads_link = item['Goodreads_Link']
            mask = (linked_URLs['Audible_Title'] == title) & (linked_URLs['Audible_Author'] == author)
            print(linked_URLs[mask])
            if len(linked_URLs[mask]) == 0:
                print('Not in Linked URLs')
                print({'Audible_Title': title, 'Audible_Author': author, 'Goodreads_Link': goodreads_link})
                linked_URLs = linked_URLs.append({'Audible_Title': title, 'Audible_Author': author, 'Goodreads_Link': goodreads_link}, ignore_index=True)
                # print(linked_URLs)
            else:
                print('Already in Linked URLs')
                continue
    return linked_URLs

linked_URLs = add_new_linked_urls(linked_URLs, book_df)
linked_URLs.to_csv(os.getcwd() + '/' + 'Linked_URLs.csv', index = False)