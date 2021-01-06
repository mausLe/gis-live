from django.urls import path, include
from . import views

urlpatterns = [
    # path("polls/", include("polls.urls")),
    path('', views.home, name="home"),
    path('location/', views.location, name="location"),
    path('history/', views.history, name="history"),


]