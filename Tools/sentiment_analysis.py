"""These are function to deal with sentiment analysis"""
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from scipy.special import softmax
import numpy as np
from typing import Tuple, Dict, List
from Tools.preprocessing import preprocessing_text

# import roberta model
roberta = 'cardiffnlp/twitter-roberta-base-sentiment'
model = AutoModelForSequenceClassification.from_pretrained(roberta)
tokenizer = AutoTokenizer.from_pretrained(roberta)


# function to extract sentiment score and label
def extract_sentiment_score(text: str) -> Tuple:
    """
    extract the sentiment score for a input text
    ----------
    param: text
    return: return tuple (labels, polarity)
        labels: can be ['Negative', 'Neutral', 'Positive']
        polarity: can be between 0 and 1
    """
    # preprocessing
    text = preprocessing_text(text)
    # extract score
    labels = ['Negative', 'Neutral', 'Positive']
    encoded_input = tokenizer(text, return_tensors='pt', max_length=512, truncation=True)
    output = model(**encoded_input)
    scores = softmax(output[0][0].detach().numpy())
    ranking = np.argsort(scores)[-1]
    l = labels[ranking]
    a = np.array([-1, 0, 1])
    polarity = sum([i * j for i, j in zip(scores, a)])
    return l, polarity
