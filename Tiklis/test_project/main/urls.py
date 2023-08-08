from django.urls import path

from . import views

urlpatterns = [
path("", views.home, name="home"),
path("home/", views.home, name="home"),
path("predict/", views.predict, name="predict"),
path("weather/", views.weather, name="weather"),
path("crops/",views.crops, name="crops"),
path("graphs/",views.graphs, name="graphs"),

]