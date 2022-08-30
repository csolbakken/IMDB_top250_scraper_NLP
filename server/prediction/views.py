from django.shortcuts import render
import pandas as pd
import joblib

def prediction_view(request):

    model = joblib.load("../model/model.pkl")

    review = pd.Series(request.GET.get("q"))
    
    y_pred = model.predict(review)
    y_pred_prob = model.predict_proba(review)

    context = {"y_pred":y_pred[0], "prob_bad":round(y_pred_prob[0][0], 2)*100, "prob_good":round(y_pred_prob[0][1], 2)*100}



    return render(request, "prediction/prediction-view.html", context=context)
