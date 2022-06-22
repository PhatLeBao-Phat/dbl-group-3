"""I just combine all the functions wrote by Xiaoya and Julie here. These are functions for preprocessing text for sentiment analysis"""

import re

"""These were written by Xiaoya"""
def cleaner(text):
    '''Remove URLs'''
    text = re.sub(r"(?:\@|http?\://|https?\://|www)\S+", "", text)
    return text


def punc(text1):
    '''Remove punctuations and symbols except ! & ?'''
    punct = '''()-[]{};:'"\,<>./@#$%^&*_~'''
    for word in text1:
        if word in punct:
            text1 = text1.replace(word, "")
    return text1

def to_lower(text2):
    '''Convert string to lower case'''
    text2 = text2.lower()
    return text2

#def emoji(text3):
    '''Convert emoji to text'''
    
def abbre(text4):
    '''Expand abbreviations, common ones'''
    abbre_dict = {"asap": "as soon as possible", "atm": "at the moment", "fyi": "for your information", "np": "no problem",
                 "pls": "please", "thx": "thanks", "lmk": "let me know", "lol": "laugh out loud", "nvm": "nevermind", 
                 "tba": "to be honest", "tbd": "to be decided"}
    for key, value in abbre_dict.items():
        text4 = text4.replace(key,value)
    return text4
    
"""These were written by Julie"""
def preproc_text(text):
    text = re.sub(r'@[^\s]+','',text) #remove quote
    text = re.sub(r'RT[\s]+',' ',text) #remove retweet
    text = re.sub(r'http\S+',' ',text) #remove hyperlink
    text = re.sub(r'www.\S+','',text) # remove web link
    text = re.sub(r'#[A-Za-z0-9_]+','',text) # remove hashtag
    text = re.sub(r'[()!?]','',text) #remove exlamation marks
    remove_list= 'Ã'+'Â'+'±'+'ã'+'¼'+'â'+'»'+'§'+ '¢‚¬¦'+ 'Å¸€¡³°Å¸€¡' + '¢‚¬Å¾'+ 'â€'+ '˜'+'™'+'ðŸ'
    table = str.maketrans('', '', remove_list)
    text = text.translate(table)
    
    text = text.split()
    del_words = ['for','of','and','to','from','on','in','at','a','an','the','am','will','would','was','were','shall']
    text = [word for word in text if not word in del_words] #remove del_words
    text = ' '.join(word for word in text)
    return text

"""This is @Phat combining everything"""

def preprocessing_text(text : str) -> str:
    """
    preprocessing text for sentiment analysis 
    ----------
    param: text: uncleaned text from tweet
    return: cleaned text
    """
    import re
    text = cleaner(text)
    text = punc(text)
    text = to_lower(text)
    text = abbre(text)
    text = preproc_text(text)

    return text 