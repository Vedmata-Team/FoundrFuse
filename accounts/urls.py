from django.urls import path, include
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

    # Django authentication URLs
    # path('accounts/', include('django.contrib.auth.urls')),

    # AJAX URLs
    path('ajax/get-states/', views.get_states, name='get_states'),
    path('ajax/get-cities/', views.get_cities, name='get_cities'),
]
