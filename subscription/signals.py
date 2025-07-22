from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils import timezone
from .models import UserSubscription, PaymentHistory
import logging

logger = logging.getLogger(__name__)

@receiver(post_save, sender=UserSubscription)
def update_user_premium_status(sender, instance, created, **kwargs):
    """
    Update user's premium status when subscription changes
    """
    # Only update if subscription is active and not expired
    if instance.is_active and instance.end_date > timezone.now():
        if not instance.user.profile.is_premium:
            instance.user.profile.is_premium = True
            instance.user.profile.save()
            logger.info(f"Premium status activated for user {instance.user.username}")
    # If subscription is inactive or expired, remove premium status
    elif instance.user.profile.is_premium:
        instance.user.profile.is_premium = False
        instance.user.profile.save()
        logger.info(f"Premium status deactivated for user {instance.user.username}")

@receiver(post_save, sender=PaymentHistory)
def handle_successful_payment(sender, instance, created, **kwargs):
    """
    Handle successful payments
    """
    if created and instance.status == 'success' and instance.subscription:
        # Ensure subscription is active
        if not instance.subscription.is_active:
            instance.subscription.is_active = True
            instance.subscription.save()
            logger.info(f"Subscription activated after payment for user {instance.user.username}")