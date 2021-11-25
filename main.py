import getData
import audible
import goodreads
import pandas as pd
import os
import settings
import read_data
import write_data
import amazon


def obj_dict(obj):
    return obj._asdict()

def main():
    df = pd.DataFrame({'Audible_Title':pd.Series([], dtype='str'), 'Audible_Subtitle':pd.Series([], dtype='str'), 'Audible_Author':pd.Series([], dtype='str'), 'Audible_Link':pd.Series([], dtype='str'), 'Image_Link':pd.Series([], dtype='str'), 'Audible_Category':pd.Series([], dtype='str'), 'Goodreads_Link':pd.Series([], dtype='str'), 'Amazon_Link':pd.Series([], dtype='str'), 'Goodreads_Rating':pd.Series([], dtype='float'), 'Number_of_Ratings':pd.Series([], dtype='int')})

    setup = getData.Setup()
    categories = setup.loadCategories(settings.IMPORT_CATEGORIES_SOURCE)
    if settings.IMPORT_CATEGORIES_SOURCE != 'bin':
        setup.saveCategories(categories)
    
    books = setup.loadBooks(settings.IMPORT_BOOKS_SOURCE, categories = categories)
    if settings.IMPORT_BOOKS_SOURCE != 'bin':
        setup.saveBooks(books)
    # Add each book to df. If it is already there, add the current book category, if it's not there.
    for book in books:
        if book.is_in_df(df):
            df = book.add_category_to_existing(book.category, df)
        else:
            book.add_to_df(df)
    
    setup.saveBooks(books)

    df.to_csv(os.getcwd() + '/data/' + settings.BOOK_FILE, index = False)

    books = read_data.get_books_from_df(df)
    
    # Get the Goodreads info, and add it to the df.
    if settings.GET_GOODREADS_RATINGS:
        books = goodreads.get_goodreads_ratings(books)
        write_data.write_column_to_df(books, df, 'Goodreads_Link', 'goodreads_link')
        write_data.write_column_to_df(books, df, 'Goodreads_Rating', 'average_rating')
        write_data.write_column_to_df(books, df, 'Number_of_Ratings', 'num_ratings')

        setup.saveBooks(books)
        df.to_csv(os.getcwd() + '/data/' + settings.BOOK_FILE, index = False)

    if settings.GET_AMAZON_LINKS:
        books = setup.getAmazonLinks(books)
        write_data.write_column_to_df(books, df, 'Amazon_Link', 'amazon_link')
        setup.saveBooks(books)
        df.to_csv(os.getcwd() + '/data/' + settings.BOOK_FILE, index = False)



    # print(books)



if __name__ == "__main__":
    main()