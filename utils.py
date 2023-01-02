import re
import pandas as pd
import os


def compare_lists(list1, list2):
    return len(set(list1).intersection(list2))


def best_row_item(list):
    """Takes a list of PossibleGoodreadsMatch objects and returns the one with the highest number of ratings"""
    # print(f'List of possibles: {list}')
    if not list:
        return None
    list_of_num_ratings = [item.goodreads_num_ratings for item in list]
    max_num_ratings = max(list_of_num_ratings)
    max_index = list_of_num_ratings.index(max_num_ratings)
    return list[max_index]


def get_tokens(string):
    string = string.replace(".", "")
    tokens = re.sub(r"[^\w\s]", "", string.replace("'", "")).strip().split()
    combined_initials = combine_initials(tokens)
    if combined_initials:
        tokens.append(combined_initials)
    return tokens


def combine_initials(list):
    initials = [initial for initial in list if len(initial) == 1]
    if initials:
        return "".join(initials)
    return None


def string_to_num(string):
    string = string.replace(",", "")
    return int(string)
