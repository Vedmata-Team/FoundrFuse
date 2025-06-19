from django.urls import path
from . import views
from .views import ChatbotAPIView

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('features/', views.features, name='features'),
    path('founders/', views.founders, name='founders'),
    path('investors/', views.investors, name='investors'),
    path('pricing/', views.pricing, name='pricing'),
    path('blog/', views.blog_list, name='blog_list'),
    path('blog/<slug:slug>/', views.blog_detail, name='blog_detail'),
    path('newsletter-signup/', views.newsletter_signup, name='newsletter_signup'),
    path('api/chatbot/', ChatbotAPIView.as_view(), name='chatbot_api'),
]
