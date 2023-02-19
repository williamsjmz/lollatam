from django.urls import path

from . import views

app_name='users'

urlpatterns = [
    path('login/', views.login, name='login'),
    path('logout/<int:user_id>/', views.logout, name='logout'),
    path('signup/', views.signup, name='signup'),
]