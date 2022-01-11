from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('signup', views.signup, name="signup"),
    path('signin', views.signin, name="signin"),
    path('signout', views.signout, name="signout"),
    path('select_genres', views.select_genres, name="select_genres"),
    path('new_recommendation', views.new_recommendation, name="new_recommendation"),
    path('dashboard', views.dashboard, name="dashboard"),
]