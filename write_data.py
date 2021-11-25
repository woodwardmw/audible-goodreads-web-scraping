import pandas as pd
import audible

def write_column_to_df(list, df, df_column, item_attribute):
    for item in list:
        if item.is_in_df(df):
            row_in_df = df.index[df['Audible_Title'].str.contains(item.title, regex = False)]
            df.loc[row_in_df, df_column] = getattr(item, item_attribute)
    return df



def main():
    """ For testing purposes"""

    df = pd.DataFrame({'Audible_Title':pd.Series([], dtype='str'), 'Audible_Subtitle':pd.Series([], dtype='str'), 'Audible_Author':pd.Series([], dtype='str'), 'Audible_Link':pd.Series([], dtype='str'), 'Image_Link':pd.Series([], dtype='str'), 'Audible_Category':pd.Series([], dtype='str'), 'Goodreads_Link':pd.Series([], dtype='str'), 'Amazon_Link':pd.Series([], dtype='str'), 'Goodreads_Rating':pd.Series([], dtype='float'), 'Number_of_Ratings':pd.Series([], dtype='int')})

    book = audible.Book(
        "A Tale Dark & Grimm",
        "Adam Gidwitz",
        "https://www.audible.com/pd/A-Tale-Dark-and-Grimm-Audiobook/0593170881?ref=a_ep_black-_c10_lProduct_1_15&pf_rd_p=1fd5ec62-ec05-48ab-a5dd-5ed59ed56551&pf_rd_r=3BWRZX00QVG28D2QJANV",
        "https://m.media-amazon.com/images/I/517e-I5cYeL._SL500_.jpg",
        " Kids & Teens, $5 Titles",
        None,
        "https://www.goodreads.com/book/show/7825557-a-tale-dark-grimm?from_search=true&from_srp=true&qid=Je0lFbkYf6&rank=1",
        None,
        None,
        None
        )
    books = []

    book.add_to_df(df)

    book = audible.Book(
            "A Tale Dark & Grimm",
            "Adam Gidwitz",
            "https://www.audible.com/pd/A-Tale-Dark-and-Grimm-Audiobook/0593170881?ref=a_ep_black-_c10_lProduct_1_15&pf_rd_p=1fd5ec62-ec05-48ab-a5dd-5ed59ed56551&pf_rd_r=3BWRZX00QVG28D2QJANV",
            "https://m.media-amazon.com/images/I/517e-I5cYeL._SL500_.jpg",
            " Kids & Teens, $5 Titles",
            None,
            "https://www.goodreads.com/book/show/7825557-a-tale-dark-grimm?from_search=true&from_srp=true&qid=Je0lFbkYf6&rank=1",
            None,
            "4.07",
            "23,228"
    )

    books.append(book)


    df = write_column_to_df(books, df, 'Goodreads_Rating', item_attribute='average_rating')
    df = write_column_to_df(books, df, 'Number_of_Ratings', item_attribute='num_ratings')

    print(df)

if __name__ == '__main__':
    main()
