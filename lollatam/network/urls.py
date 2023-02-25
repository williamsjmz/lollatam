from django.urls import path

from . import views

app_name='network'

urlpatterns = [
    path('profile/', views.profile, name='profile'),
]