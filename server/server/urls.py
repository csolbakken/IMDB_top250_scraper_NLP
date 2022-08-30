from django.contrib import admin
from django.urls import path
from .views import home_view
from prediction import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", home_view),
    path("prediction/", views.prediction_view)
]
