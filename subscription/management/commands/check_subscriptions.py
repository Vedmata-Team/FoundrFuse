from django.core.management.base import BaseCommand
from django.utils import timezone
from subscription.models import UserSubscription
from django.db.models import Q

class Command(BaseCommand):
    help = 'Check and update subscription statuses'

    def handle(self, *args, **kwargs):
        # Find subscriptions that are active but have expired
        expired_subscriptions = UserSubscription.objects.filter(
            Q(is_active=True) & Q(end_date__lte=timezone.now())
        )
        
        count = 0
        for subscription in expired_subscriptions:
            subscription.is_active = False
            subscription.user.profile.is_premium = False
            subscription.user.profile.save()
            subscription.save()
            count += 1
            
        self.stdout.write(
            self.style.SUCCESS(f'Successfully deactivated {count} expired subscriptions')
        )