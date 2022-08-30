from django.shortcuts import render
from review_database.models import Review
import random as rd

def home_view(request):

    random_review = Review.objects.get(id=rd.randint(1, 5000))
    print(random_review)

    context = {"review":random_review}


    return render(request, "home-view.html", context=context)
    