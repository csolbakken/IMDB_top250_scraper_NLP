import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.model_selection import GridSearchCV

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS


import warnings
import joblib


warnings.filterwarnings("ignore", category=DeprecationWarning)


def model_():
    def loading_preprocessing():
        df = pd.read_csv("model/data/reviews_data.csv")
        df.set_index("index", inplace=True)
        df.drop(columns=["Unnamed: 0"], inplace=True)

        mapper = {1:"bad", 2:"bad", 3:"bad", 4:"bad", 5:"bad", 6:"good", 7:"good", 8:"good", 9:"good", 10:"good"}
        df["ratings"] = df["ratings"].replace(mapper)

        X_train, X_test, y_train, y_test = train_test_split(df.drop(columns='ratings'),df['ratings'], test_size=0.15, random_state=42)

        return X_train, X_test, y_train, y_test


    def gridsearch(X_train, y_train):
        pipe = Pipeline ([ ('tokenizer', TfidfVectorizer(min_df=0.01, max_df=0.9, stop_words="english")),
                             ('classifier',  LogisticRegression(solver='saga'))
                          ] )


        param_grid = [
                      {"classifier": [LogisticRegression(solver="saga")],
                       "tokenizer__ngram_range": [(1, 1), (1, 2), (1, 3)],
                        "classifier__C": [0.01, 0.1, 1]}]


        grid = GridSearchCV(pipe, param_grid, cv=5)
        grid.fit(X_train.reviews, y_train)

        return grid
    
    X_train, X_test, y_train, y_test = loading_preprocessing()
    model = gridsearch(X_train, y_train)
    
    ## Save the model
    joblib.dump(model, 'model/model.pkl')

    ## Save the testing set
    X_test.to_csv("model/data/x_test.csv")
    y_test.to_csv("model/data/y_test.csv")
 

model_()
        
        



