"""functions that help deal with conversations"""
import pandas as pd 
import numpy as np 


def start_end_customers_filter(df : pd.DataFrame) -> pd.DataFrame:
    """
    filter each conversation with the start and end tweets by customers 
    ---------
    param: df : conversation dataframe with all the id of tweets in a conversation
    return: a df with 2 attributes 
        open_tweet_sentiment : score of tweet at the start of conversation by customers
        closed_tweet_sentiment : score of tweet at the end of conversation by customers 
    """
    lst_open = []
    lst_close = []
    for index, row in df.iterrows():
        # get id of the opening
        if row.conversation_opener == 'customer':
            open = row.id_1
            if pd.notna(row.id_7):
                close = row.id_7
            elif pd.notna(row.id_5):
                close = row.id_5
            else:
                close = row.id_3
        else:
            open = row.id_2
            if pd.notna(row.id_6):
                close = row.id_6
            else:
                close = row.id_4
        lst_open.append(open)
        lst_close.append(close)
    
    open_close_df = pd.DataFrame({
        'open' : lst_open,
        'close' : lst_close
    })
    return open_close_df
    