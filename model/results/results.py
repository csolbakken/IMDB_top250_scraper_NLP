import pandas as pd
import joblib

from sklearn.metrics import confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt


def results_():

    ## Prediction
    def predict():
        model = joblib.load('model/model.pkl')
        X_test = pd.read_csv('model/data/X_test.csv')
        y_test = pd.read_csv('model/data/y_test.csv')
        y_pred = model.predict(X_test.reviews)
        return y_test.ratings, y_pred

    ## Confusion Matrix
    def get_cm(y_test, y_pred):
        cf_matrix = confusion_matrix(y_test, y_pred)

        ax = sns.heatmap(cf_matrix, annot=True, cmap='Blues', fmt='g')

        ax.set_title('Confusion Matrix');
        ax.set_xlabel('Predicted Value')
        ax.set_ylabel('True Value');

        ax.xaxis.set_ticklabels(['Bad','Good'])
        ax.yaxis.set_ticklabels(['Bad','Good'])


        plt.savefig('model/results/ConfusionMatrix.png')

    y_test, y_pred = predict()
    get_cm(y_test, y_pred)


results_()



