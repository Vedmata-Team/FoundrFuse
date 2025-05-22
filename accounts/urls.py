from django.urls import path
from . import views

urlpatterns = [
    path('join-beta/', views.join_beta, name='join_beta'),
    path('login/', views.login_view, name='login'),
]