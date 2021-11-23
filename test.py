import audible
import pandas as pd

df = pd.DataFrame({'Audible_Title':pd.Series([], dtype='str'), 'Audible_Subtitle':pd.Series([], dtype='str'), 'Audible_Author':pd.Series([], dtype='str'), 'Audible_Link':pd.Series([], dtype='str'), 'Image_Link':pd.Series([], dtype='str'), 'Audible_Category':pd.Series([], dtype='str'), 'Goodreads_Link':pd.Series([], dtype='str'), 'Amazon_Link':pd.Series([], dtype='str'), 'Goodreads_Rating':pd.Series([], dtype='float'), 'Number_of_Ratings':pd.Series([], dtype='int')})


book1 =  audible.Book(
        "The Huntress",
        "Kate Quinn",
        "https://www.audible.com/pd/The-Huntress-Audiobook/006289482X?ref=a_ep_black-_c10_lProduct_1_1&pf_rd_p=ebb303be-30a4-4f6e-bec6-a7604e9f0c63&pf_rd_r=R0EJM3GY7J7FM6JE1HKD",
        "https://m.media-amazon.com/images/I/51TptSvhIWL._SL500_.jpg",
        ["Fiction"],
        "A Novel",
        None,
        None,
        None,
        None)
book2 = audible.Book(
        "Mrs. Everything",
        "Jennifer Weiner",
        "https://www.audible.com/pd/Mrs-Everything-Audiobook/1508251800?ref=a_ep_black-_c10_lProduct_1_2&pf_rd_p=ebb303be-30a4-4f6e-bec6-a7604e9f0c63&pf_rd_r=R0EJM3GY7J7FM6JE1HKD",
        "https://m.media-amazon.com/images/I/41chzE2cibL._SL500_.jpg",
        ["Fiction"],
        "A Novel",
        None,
        None,
        None,
        None
)

book1.add_to_df(df)

print(book1)
print(df)
print(book1.is_in_df(df))
print(book2.is_in_df(df))
book2.add_to_df(df)
book1.add_category("test", df)
book2.add_category('test_2', df)
print(df)
print(df.index[df['Audible_Title'].str.contains(book1.title, regex = False)])
print(book1)
print(df['Audible_Category'])