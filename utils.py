import re

def compare_lists(list1, list2):
    return len(set(list1).intersection(list2))

def best_row_item(list):
    """Takes a list of PossibleGoodreadsMatch objects and returns the one with the highest number of ratings"""
    if not list:
        return None
    max_num_ratings = max(item.goodreads_num_ratings for item in list)
    max_index = list.index(max_num_ratings)
    return list[max_index]

def get_tokens(string):
    return re.sub(r'[^\w\s]','',string.replace("'", "")).strip().split()