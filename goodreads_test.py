import pytest
import asyncio 

import pandas as pd

import goodreads, read_data

async def test_get_goodreads_ratings():
    df = pd.read_csv('fixtures/audible_books.csv')
    books = read_data.get_books_from_df(df)
    books = await goodreads.get_goodreads_ratings(books)
    ratings = [book.average_rating for book in books if book.average_rating]
    print(ratings)

    assert len(ratings) > len(df.index) / 2  # Make sure at least half of ratings are being found
    assert sum(ratings) > len(ratings) * 3.0
    assert sum(ratings) < len(ratings) * 4.5

if __name__ == '__main__':
    asyncio.run(test_get_goodreads_ratings())
    # for task in asyncio.Task.all_tasks():
    #     print(task)