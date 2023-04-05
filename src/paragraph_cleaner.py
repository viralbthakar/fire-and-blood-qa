import string
import pandas as pd
from collections import defaultdict

from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer


class ParagraphCleaner(object):
    def __init__(self, dataframe, in_column, out_column):
        self.dataframe = dataframe
        self.in_column = in_column
        self.out_column = out_column

    def remove_punctuation(self, text, punctuation=','):
        text = text.replace(punctuation, '')
        return text

    def lowercase(self, text):
        text = text.lower()
        return text

    def remove_numbers(self, text):
        text = ''.join([i for i in text if not i.isdigit()])
        return text

    def remove_stopwords(self, text, language='english'):
        stop_words = set(stopwords.words(language))
        tokenized = word_tokenize(text)
        text = [
            word for word in tokenized if not word in stop_words]
        text = " ".join(text)
        return text

    def lemmatize(self, text):
        lemmatizer = WordNetLemmatizer()  # Instantiate lemmatizer
        text = [lemmatizer.lemmatize(word) for word in text]  # Lemmatize
        text = " ".join(text)
        return text

    def clean_data(self):
        self.dataframe[self.out_column] = self.dataframe[self.in_column].apply(
            self.remove_punctuation)
        self.dataframe[self.out_column] = self.dataframe[self.out_column].apply(
            self.remove_stopwords)
        return self.dataframe
