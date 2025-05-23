from django.urls import path
from . import views

urlpatterns = [
    path('', views.subscription_home, name='home'),
    path('upgrade/', views.upgrade, name='upgrade'),
    path('history/', views.payment_history, name='history'),
    path('checkout/<int:plan_id>/', views.checkout, name='checkout'),
    path('success/', views.payment_success, name='payment_success'),
    path('cancel/', views.payment_cancel, name='payment_cancel'),
]
