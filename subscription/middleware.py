from django.utils import timezone
from .models import UserSubscription

class SubscriptionMiddleware:
    """
    Middleware to check subscription status on each request
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check subscription status only for authenticated users
        if request.user.is_authenticated:
            # Get user's active subscription
            subscription = UserSubscription.objects.filter(
                user=request.user,
                is_active=True
            ).first()
            
            # If subscription exists, check if it's expired
            if subscription and subscription.end_date <= timezone.now():
                subscription.check_status()
        
        response = self.get_response(request)
        return response