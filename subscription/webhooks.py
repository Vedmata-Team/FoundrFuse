from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import hmac
import hashlib
import json
import logging
from django.conf import settings
from django.contrib.auth.models import User
from .models import UserSubscription, PaymentHistory, SubscriptionPlan

logger = logging.getLogger(__name__)

@csrf_exempt
def razorpay_webhook(request):
    if request.method == 'POST':
        data = request.body
        received_signature = request.headers.get('X-Razorpay-Signature')

        # Make sure RAZORPAY_WEBHOOK_SECRET is set in settings
        if not hasattr(settings, 'RAZORPAY_WEBHOOK_SECRET'):
            logger.error("RAZORPAY_WEBHOOK_SECRET not set in settings")
            return HttpResponse("Configuration error", status=500)

        secret = settings.RAZORPAY_WEBHOOK_SECRET.encode()
        generated_signature = hmac.new(secret, data, hashlib.sha256).hexdigest()

        if hmac.compare_digest(received_signature, generated_signature):
            payload = json.loads(data)
            logger.info(f"Webhook received: {payload['event']}")

            try:
                if payload['event'] == 'payment.captured':
                    payment_entity = payload['payload']['payment']['entity']
                    payment_id = payment_entity['id']
                    amount = payment_entity['amount'] / 100  # Convert from paise to rupees
                    
                    # Get user and plan from notes
                    notes = payment_entity.get('notes', {})
                    user_id = notes.get('user_id')
                    plan_id = notes.get('plan_id')
                    
                    if user_id and plan_id:
                        try:
                            user = User.objects.get(id=user_id)
                            plan = SubscriptionPlan.objects.get(id=plan_id)
                            
                            # Check for existing payment to avoid duplicates
                            if not PaymentHistory.objects.filter(payment_id=payment_id).exists():
                                # Check for existing subscription
                                existing_sub = UserSubscription.objects.filter(
                                    user=user, is_active=True
                                ).first()
                                
                                if existing_sub and existing_sub.plan == plan:
                                    # Renew existing subscription
                                    existing_sub.renew()
                                    subscription = existing_sub
                                elif existing_sub:
                                    # Deactivate old subscription
                                    existing_sub.is_active = False
                                    existing_sub.save()
                                    
                                    # Create new subscription
                                    subscription = UserSubscription.objects.create(
                                        user=user,
                                        plan=plan,
                                        start_date=timezone.now(),
                                        is_active=True
                                    )
                                else:
                                    # Create new subscription
                                    subscription = UserSubscription.objects.create(
                                        user=user,
                                        plan=plan,
                                        start_date=timezone.now(),
                                        is_active=True
                                    )
                                
                                # Record payment
                                PaymentHistory.objects.create(
                                    user=user,
                                    subscription=subscription,
                                    payment_id=payment_id,
                                    amount=amount,
                                    status='success'
                                )
                                
                                # Update user's premium status
                                user.profile.is_premium = True
                                user.profile.save()
                                
                                logger.info(f"Subscription activated for user {user.username}")
                        except User.DoesNotExist:
                            logger.error(f"User with ID {user_id} not found")
                        except SubscriptionPlan.DoesNotExist:
                            logger.error(f"Plan with ID {plan_id} not found")
                    else:
                        logger.error("Missing user_id or plan_id in payment notes")
                        
                elif payload['event'] == 'subscription.charged':
                    # Handle recurring subscription payments
                    subscription_entity = payload['payload']['subscription']['entity']
                    # Process recurring payment logic here
                    logger.info(f"Subscription charged: {subscription_entity['id']}")
                    
            except Exception as e:
                logger.error(f"Error processing webhook: {str(e)}")
                return HttpResponse(str(e), status=500)
                
            return HttpResponse(status=200)
        else:
            logger.warning("Invalid webhook signature")
            return HttpResponse("Invalid signature", status=400)

    return HttpResponse("Only POST method allowed", status=405)
