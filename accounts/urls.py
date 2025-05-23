from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Authentication URLs
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),
    
    # Profile URLs
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    
    # Matching URLs
    path('discover/', views.discover, name='discover'),
    path('matches/', views.matches, name='matches'),
    path('swipe/<int:profile_id>/<str:action>/', views.swipe_action, name='swipe_action'),
    
    # Waitlist
    path('waitlist/', views.waitlist, name='waitlist'),
]
