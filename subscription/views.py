from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta
from .models import SubscriptionPlan, UserSubscription, PaymentHistory
import uuid
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.conf import settings
from django.utils import timezone
from django.contrib import messages
from datetime import timedelta
import razorpay 
import uuid

from .models import SubscriptionPlan, UserSubscription, PaymentHistory
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

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.conf import settings
from django.utils import timezone
from django.contrib import messages
from datetime import timedelta
import razorpay
import uuid

from .models import SubscriptionPlan, UserSubscription, PaymentHistory

@login_required
def checkout(request, plan_id):
    plan = get_object_or_404(SubscriptionPlan, id=plan_id, is_active=True)

    # Razorpay client
    client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

    # Create Razorpay order
    razorpay_order = client.order.create({
        "amount": int(plan.price * 100),  # in paise
        "currency": "INR",
        "payment_capture": 1,
        "notes": {
            "user_id": str(request.user.id),
            "plan_id": str(plan.id),
            "user_email": request.user.email
        }
    })

    # Store order id temporarily in session or DB if needed for later verification
    request.session['razorpay_order_id'] = razorpay_order['id']
    request.session['plan_id'] = plan.id

    context = {
        'title': 'Checkout',
        'plan': plan,
        'razorpay_order_id': razorpay_order['id'],
        'razorpay_key_id': settings.RAZORPAY_KEY_ID,
        'amount': razorpay_order['amount'],
        'user_email': request.user.email,
        'user_name': request.user.get_full_name() or request.user.username,
    }

    return render(request, 'subscription/checkout.html', context)

from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
@login_required
def payment_verify(request):
    payment_id = request.GET.get("payment_id")
    order_id = request.GET.get("order_id")
    signature = request.GET.get("signature")
    plan_id = request.session.get('plan_id')

    client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

    try:
        # Verify the signature
        client.utility.verify_payment_signature({
            'razorpay_order_id': order_id,
            'razorpay_payment_id': payment_id,
            'razorpay_signature': signature
        })

        # Get the plan
        plan = SubscriptionPlan.objects.get(id=plan_id)

        # Create subscription & record payment
        subscription = UserSubscription.objects.create(
            user=request.user,
            plan=plan,
            start_date=timezone.now(),
            end_date=timezone.now() + timedelta(days=plan.duration_months * 30),
            is_active=True
        )

        PaymentHistory.objects.create(
            user=request.user,
            subscription=subscription,
            payment_id=payment_id,
            amount=plan.price,
            status='success'
        )

        request.user.profile.is_premium = True
        request.user.profile.save()

        messages.success(request, "Payment successful! Your subscription has been activated.")
        return redirect('subscription:payment_success')

    except razorpay.errors.SignatureVerificationError:
        messages.error(request, "Payment verification failed. Please try again.")
        return redirect('subscription:checkout', plan_id=plan_id)

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
