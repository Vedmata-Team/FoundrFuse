from django.utils import timezone
from .models import UserSubscription
from django.db.models import Q
import logging

logger = logging.getLogger(__name__)

def check_expired_subscriptions():
    """
    Check for expired subscriptions and deactivate them
    This can be run as a scheduled task (e.g., with Celery)
    """
    # Find subscriptions that are active but have expired
    expired_subscriptions = UserSubscription.objects.filter(
        Q(is_active=True) & Q(end_date__lte=timezone.now())
    )
    
    count = 0
    for subscription in expired_subscriptions:
        try:
            subscription.is_active = False
            subscription.user.profile.is_premium = False
            subscription.user.profile.save()
            subscription.save()
            count += 1
            logger.info(f"Deactivated expired subscription for user {subscription.user.username}")
        except Exception as e:
            logger.error(f"Error deactivating subscription: {str(e)}")
    
    logger.info(f"Deactivated {count} expired subscriptions")
    return count