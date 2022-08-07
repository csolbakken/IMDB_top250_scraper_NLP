import pandas as pd
import numpy as np
import joblib

from sklearn.metrics import confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt

def main():

    ## Prediction
    def predict():
        model = joblib.load('model.pkl')
        X_test = pd.read_csv('data/X_test.csv')
        y_test = pd.read_csv('data/y_test.csv')
        y_pred = model.predict(X_test)

        return y_test, y_pred

    ## Confusion Matrix
    def get_cm(y_test, y_pred):
        cf_matrix = confusion_matrix(y_test, y_pred)

        ax = sns.heatmap(cf_matrix, annot=True, cmap='Blues')

        ax.set_title('Confusion Matrixn\n');
        ax.set_xlabel('\nPredicted Value')
        ax.set_ylabel('True Value');

        ax.xaxis.set_ticklabels(['False','True'])
        ax.yaxis.set_ticklabels(['False','True'])

        plt.savefig('model/ConfusionMatrix.png')

    y_test, y_pred = predict()
    get_cm(y_test, y_pred)






