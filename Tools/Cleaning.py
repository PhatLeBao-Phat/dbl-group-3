import pandas as pd
import json
import numpy as np
import sqlite3
from typing import List, Dict, Tuple
from definitions.airlines import airlines_id, airlines_name


def remove_duplicated_text(df_data: pd.DataFrame) -> pd.DataFrame:
    """
    Function to remove duplicated datapoints that send by users but not airlines.
    Tweets are considered to be a duplicate if they are sent by the same user to the same tweet.
    This function resets index.

    parameter: df_data: DataFrame
    return: DataFrame
    """
    # remove duplicated tweets sent by users not KLM or Bri
    df_tweets = df_data.reset_index(drop=True)
    df_tweets = df_tweets.dropna(subset=['user'])
    du = df_tweets.duplicated(subset=['text', 'user_id', 'in_reply_to_status_id'])
    # get a list index of duplicated text (datapoint)
    lst = [index for index, values in du.items() if values == True]
    # define airline dictionary
    airline = {
        'KLM': 56377143,
        'AirFrance': 106062176,
        'British_Airways': 18332190,
        'AmericanAir': 22536055,
        'Lufthansa': 124476322,
        'AirBerlin': 26223583,
        'AirBerlin assist': 2182373406,
        'easyJet': 38676903,
        'RyanAir': 1542862735,
        'SingaporeAir': 253340062,
        'Qantas': 218730857,
        'EtihadAirways': 45621423,
        'VirginAtlantic': 20626359
    }
    # drop the duplicated texts that not from any airlines
    drop_lst = []
    for i in lst:
        if df_tweets.loc[i, 'user_id'] not in airline.values():
            drop_lst.append(i)
    df_tweets.drop(index=drop_lst, inplace=True)
    return df_tweets


def reset_index(df_data: pd.DataFrame) -> pd.DataFrame:
    """
    reset the index when pull the non-name column from database
    resulting from doing query like SELECT * FROM general_tweets
    """
    return df_data.set_index('', inplace=True)


def drop_invalid_reply(df: pd.DataFrame) -> pd.DataFrame:
    """
    some tweets that are not a reply have non-NA value in one of 2 attributes in_reply_to_user_id or in_reply_to_status_id
    therefore, we have to drop them 
    """
    try:
        reply_user = pd.isna(df['in_reply_to_user_id'])
        reply_status = pd.isna(df['in_reply_to_status_id'])
        a = (reply_user == True) & (reply_status == False)
        b = (reply_user == False) & (reply_status == True)
        return df[np.invert(a | b)]
    except KeyError:
        print("missing one of 2 attributes in_reply_to_user_id or in_reply_to_status_id")


# filter only one that have the at least one person in 2 persons is an airline
def filter_non_airlines_conversation(lst: List[str], df: pd.DataFrame, airlines_id: Dict) -> pd.DataFrame:
    """
    Drop conversations that don't have at least 1 person is an airline account

    Parameters
    ----------
    lst : a list of string name of 2 attributes. For example: ['first_person_id', 'second_person_id']
    df : DataFrame contains conversation
    airlines_id : the dictionary of airlines. Example {'KLM' : 12231421}. We can import from definitions folder

    Returns
    ----------
    df : cleaned df
    """
    df_out = df.copy()
    bol_lst = df_out[lst[0]].isin(airlines_id.values()) | (df_out[lst[1]].isin(airlines_id.values()))
    df_out = df_out[bol_lst]
    return df_out


# build 2 new attributes to identify conversations below to which airlines
def add_airlines_id(df: pd.DataFrame, lst: List[str]) -> pd.DataFrame:
    """
    add the name of the airlines and its id to the conversations

    Parameters:
    -----------
    df : dataframe
    lst : list name of 2 attributes

    Returns:
    ----------
    df with an attribute indicating which airline and an attribute indicating that airline's id
    """
    df_out = df.copy()
    airline_lst = []
    airline_name_lst = []
    for index, row in df_out.iterrows():
        try:
            airline_name_lst.append(airlines_name[row[lst[0]]])
            airline_lst.append(row[lst[0]])
        except:
            airline_name_lst.append(airlines_name[row[lst[1]]])
            airline_lst.append(row[lst[1]])
    df_out['airline_id'] = airline_lst
    df_out['airline_name'] = airline_name_lst

    return df_out


def change_type(df: pd.DataFrame) -> pd.DataFrame:
    """
    change types in the dataframe queried from database back to the type you need
    you can also doing .dtypes() function for each attributes
    :param df: general tweet dataframe
    :return: correct df
    """
    dct = {
        'created_at': 'datetime64[ns, UTC]',
        'id': 'float64',
        'id_str': 'float64',
        'text': 'object',
        'display_text_range': 'object',
        'source': 'object',
        'truncated': 'float64',
        'in_reply_to_status_id': 'float64',
        'in_reply_to_status_id_str': 'float64',
        'in_reply_to_user_id': 'float64',
        'in_reply_to_user_id_str': 'float64',
        'in_reply_to_screen_name': 'object',
        'user': 'object',
        'geo': 'object',
        'coordinates': 'object',
        'place': 'object',
        'contributors': 'float64',
        'is_quote_status': 'float64',
        'quote_count': 'float64',
        'reply_count': 'float64',
        'retweet_count': 'float64',
        'favorite_count': 'float64',
        'entities': 'object',
        'extended_entities': 'object',
        'favorited': 'float64',
        'retweeted': 'float64',
        'possibly_sensitive': 'float64',
        'filter_level': 'object',
        'lang': 'object',
        'timestamp_ms': 'datetime64[ns]',
        'retweeted_status': 'object',
        'extended_tweet': 'object',
        'quoted_status_id': 'float64',
        'quoted_status_id_str': 'float64',
        'quoted_status': 'object',
        'quoted_status_permalink': 'object',
        'delete': 'object',
        'user_id': 'int64'
    }
    for key in dct.keys():
        try:
            df = df.astype({key: dct[key]})
        except:
            pass

    return df