import pandas as pd
import os
import audible

def get_books_from_df(df):
    books = []
    for index, row in df.iterrows():
        book = audible.Book(row['Audible_Title'], row['Audible_Author'], row['Audible_Link'], row['Image_Link'], row['Audible_Category'], subtitle = row['Audible_Subtitle'], goodreads_link = row['Goodreads_Link'], amazon_link = row['Amazon_Link'], average_rating = row['Goodreads_Rating'], num_ratings = row['Number_of_Ratings'])
        books.append(book)
    return books
    
df = pd.read_csv(os.getcwd() + '/' + 'Black_Friday_Sale_Nov_2021.csv')
books = get_books_from_df(df)
print(books[1])
