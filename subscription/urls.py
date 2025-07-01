from django.urls import path
from . import views
from .webhooks import razorpay_webhook

urlpatterns = [
    path('', views.subscription_home, name='home'),
    path('upgrade/', views.upgrade, name='upgrade'),
    path('verify/', views.payment_verify, name='payment_verify'),
    path('history/', views.payment_history, name='payment_history'),
    path('checkout/<int:plan_id>/', views.checkout, name='checkout'),
    path('success/', views.payment_success, name='payment_success'),
    path('cancel/', views.payment_cancel, name='payment_cancel'),
    path('webhook/razorpay/', razorpay_webhook, name='razorpay_webhook'),
]
