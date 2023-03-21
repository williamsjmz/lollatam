from django.urls import path

from . import views
from .API import views as api_views

app_name='search'

urlpatterns = [
    path('', views.index, name='index'),

    # API Routes
    path('stats/<str:server>/<str:summoner>/', api_views.get_summoner_stats, name='get_summoner_stats'),
]