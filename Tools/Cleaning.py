import pandas as pd
import json
import numpy as np
import sqlite3


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
