from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta
from .models import SubscriptionPlan, UserSubscription, PaymentHistory
import uuid

@login_required
def subscription_home(request):
    # Check if user has an active subscription
    user_subscription = UserSubscription.objects.filter(
        user=request.user,
        is_active=True,
        end_date__gt=timezone.now()
    ).first()
    
    # Get all available plans
    plans = SubscriptionPlan.objects.filter(is_active=True)
    
    return render(request, 'subscription/home.html', {
        'title': 'Subscription',
        'user_subscription': user_subscription,
        'plans': plans,
    })

@login_required
def upgrade(request):
    # Get all available plans
    plans = SubscriptionPlan.objects.filter(is_active=True)
    
    # Check if user has an active subscription
    user_subscription = UserSubscription.objects.filter(
        user=request.user,
        is_active=True,
        end_date__gt=timezone.now()
    ).first()
    
    return render(request, 'subscription/upgrade.html', {
        'title': 'Upgrade to Premium',
        'plans': plans,
        'user_subscription': user_subscription,
    })

@login_required
def checkout(request, plan_id):
    plan = get_object_or_404(SubscriptionPlan, id=plan_id, is_active=True)
    
    if request.method == 'POST':
        # This is just a simulation of payment processing
        # In a real app, you would integrate with a payment gateway like Stripe
        
        # Create a new subscription
        subscription = UserSubscription.objects.create(
            user=request.user,
            plan=plan,
            start_date=timezone.now(),
            end_date=timezone.now() + timedelta(days=plan.duration_months * 30),
            is_active=True
        )
        
        # Create payment record
        payment = PaymentHistory.objects.create(
            user=request.user,
            subscription=subscription,
            payment_id=str(uuid.uuid4()),
            amount=plan.price,
            status='success'
        )
        
        # Update user's premium status
        request.user.profile.is_premium = True
        request.user.profile.save()
        
        messages.success(request, f'Thank you for upgrading to {plan.name}! Your subscription is now active.')
        return redirect('subscription:payment_success')
    
    return render(request, 'subscription/checkout.html', {
        'title': 'Checkout',
        'plan': plan,
    })

@login_required
def payment_history(request):
    # Get user's payment history
    payments = PaymentHistory.objects.filter(user=request.user).order_by('-payment_date')
    
    return render(request, 'subscription/history.html', {
        'title': 'Payment History',
        'payments': payments,
    })

@login_required
def payment_success(request):
    return render(request, 'subscription/success.html', {'title': 'Payment Successful'})

@login_required
def payment_cancel(request):
    messages.warning(request, 'Your payment was cancelled.')
    return redirect('subscription:upgrade')
