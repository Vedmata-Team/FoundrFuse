from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta

class SubscriptionPlan(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration_months = models.PositiveIntegerField(default=1)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name} (${self.price}/{self.duration_months} month{'s' if self.duration_months > 1 else ''})"

class UserSubscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subscriptions')
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.SET_NULL, null=True, related_name='subscribers')
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username}'s {self.plan.name} Subscription"
    
    def save(self, *args, **kwargs):
        # Set end date based on plan duration if it's not set
        if not self.end_date:
            self.end_date = self.start_date + timedelta(days=self.plan.duration_months * 30)
        
        # Update user's premium status
        if self.is_active and self.end_date > timezone.now():
            self.user.profile.is_premium = True
            self.user.profile.save()
        
        super().save(*args, **kwargs)
    
    def check_status(self):
        """Check if subscription is still active based on end_date"""
        if self.end_date <= timezone.now():
            self.is_active = False
            self.user.profile.is_premium = False
            self.user.profile.save()
            self.save()
        return self.is_active

class PaymentHistory(models.Model):
    PAYMENT_METHOD_CHOICES = (
        ('razorpay', 'Razorpay'),
        ('stripe', 'Stripe'),
        ('paypal', 'PayPal'),
        ('manual', 'Manual'),
    )

    STATUS_CHOICES = (
        ('success', 'Success'),
        ('failed', 'Failed'),
        ('pending', 'Pending'),
        ('refunded', 'Refunded'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payments')
    subscription = models.ForeignKey(UserSubscription, on_delete=models.SET_NULL, null=True, related_name='payments')
    payment_id = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, default='razorpay')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    payment_date = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name_plural = 'Payment Histories'

    def __str__(self):
        return f"{self.user.username}'s payment of ${self.amount} - {self.status}"