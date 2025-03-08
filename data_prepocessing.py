import pandas as pd
import streamlit as st
import re
from nltk.tokenize import TweetTokenizer
import nltk
import string
from nltk.corpus import stopwords

# Remove Duplicate
def remove_duplicates(df, subset_column):
    df_no_duplicate = df.drop_duplicates(subset=[subset_column])
    return df_no_duplicate

# Text Cleaning
regex_options = {
    "URL": r'https?://\S+|www\.\S+',
    "Hashtag": r'#',
    "Remove Account": r'@\w+\s*',
    "Mention": r'@',
    "Weird Pattern (&amp)": r'&amp',
    "Date": r'\(\d{1,2}/\d{1,2}/\d{4}\)',
    "Outside A-Z, a-z, and 0-9": r'[^A-Za-z0-9?!@\s]'
}
def clean_text_column(dataframe, column_name, selected_regex):
    for pattern in selected_regex:
        if pattern in regex_options:
            dataframe[column_name] = dataframe[column_name].apply(lambda x: re.sub(regex_options[pattern], '', x))
    return dataframe

# Remove Stopwords
id_stopwords = stopwords.words('indonesian')

def setup_custom_stopwords(sw_input):
    if sw_input :
        more_stopwords = [word.strip() for word in sw_input.split(",")]
    else :
        more_stopwords = []

    custom_stopwords = id_stopwords + more_stopwords
    return custom_stopwords

def remove_stopwords(text, custom_stopwords):
    tokenizer = TweetTokenizer(preserve_case=False)
    text_tokens = tokenizer.tokenize(text)

    text_clean = []
    for word in text_tokens:
        if word not in custom_stopwords:
            text_clean.append(word)
    
    return " ".join(text_clean)

def remove_null_values(df, subset=None):
    if subset:
        df = df.dropna(subset=subset)

    return df
