import asyncio
import argparse
import getpass
from pathlib import Path

import pandas as pd

import settings
import getData
import goodreads
import read_data
import write_data


def fill_missing_ratings(df, csv_filepath):
    df_no_ratings = df[df["Goodreads_Link"].isnull()]
    print(df_no_ratings)
    remaining = len(df_no_ratings.index)
    while remaining > 0:
        print(f"Remaining null ratings: {remaining}")
        df_sample = df_no_ratings.head(40)
        books = read_data.get_books_from_df(df_sample)
        # Get the Goodreads info, and add it to the df.
        books = asyncio.run(goodreads.get_goodreads_ratings(books))
        print(books)
        write_data.write_column_to_df(books, df, "Goodreads_Link", "goodreads_link")
        write_data.write_column_to_df(books, df, "Goodreads_Rating", "average_rating")
        write_data.write_column_to_df(books, df, "Number_of_Ratings", "num_ratings")

        df.to_csv(csv_filepath, index=False)
        df_no_ratings = df[df["Goodreads_Link"].isnull()]
        remaining = len(df_no_ratings.index)


def main(args):
    csv_filepath = Path(f"data/{settings.BOOK_FILE}")
    if csv_filepath.exists():
        df = pd.read_csv(csv_filepath)
    else:
        df = pd.DataFrame(
            {
                "Audible_Title": pd.Series([], dtype="str"),
                "Audible_Subtitle": pd.Series([], dtype="str"),
                "Audible_Author": pd.Series([], dtype="str"),
                "Audible_Link": pd.Series([], dtype="str"),
                "Image_Link": pd.Series([], dtype="str"),
                "Audible_Category": pd.Series([], dtype="str"),
                "Goodreads_Link": pd.Series([], dtype="str"),
                "Amazon_Link": pd.Series([], dtype="str"),
                "Goodreads_Rating": pd.Series([], dtype="float"),
                "Number_of_Ratings": pd.Series([], dtype="int"),
            }
        )

        setup = getData.Setup(username=args.username, password=args.password)
        categories = setup.loadCategories(settings.IMPORT_CATEGORIES_SOURCE)
        if settings.IMPORT_CATEGORIES_SOURCE != "bin":
            setup.saveCategories(categories)

        books = setup.loadBooks(settings.IMPORT_BOOKS_SOURCE, categories=categories)
        if settings.IMPORT_BOOKS_SOURCE != "bin":
            setup.saveBooks(books)
        # Add each book to df. If it is already there, add the current book category, if it's not there.
        for book in books:
            if book.is_in_df(df):
                df = book.add_category_to_existing(book.category, df)
            else:
                book.add_to_df(df)

        setup.saveBooks(books)

        df.to_csv(csv_filepath, index=False)

    df = fill_missing_ratings(df, csv_filepath)

    if settings.GET_AMAZON_LINKS:
        books = setup.getAmazonLinks(books)
        write_data.write_column_to_df(books, df, "Amazon_Link", "amazon_link")
        setup.saveBooks(books)
        df.to_csv(csv_filepath, index=False)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--username", help="Username for Audible login")
    parser.add_argument("--password", help="Password for Audible login. Can be left blank and entered after running the script so it's not visible on the screen.")
    args = parser.parse_args()
    if not args.password:
        args.password = getpass.getpass()
    main(args)
