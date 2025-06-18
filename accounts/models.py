from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    USER_TYPES = (
        ('founder', 'Founder'),
        ('investor', 'Investor'),
    )

    INDUSTRY_CHOICES = (
        ('tech', 'Technology'),
        ('health', 'Healthcare'),
        ('finance', 'Finance'),
        ('education', 'Education'),
        ('ecommerce', 'E-Commerce'),
        ('real_estate', 'Real Estate'),
        ('food', 'Food & Beverage'),
        ('travel', 'Travel'),
        ('other', 'Other'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=10, choices=USER_TYPES)
    bio = models.TextField(blank=True)
    company_name = models.CharField(max_length=100, blank=True)
    industry = models.CharField(max_length=20, choices=INDUSTRY_CHOICES, blank=True)
    location = models.CharField(max_length=100, blank=True)
    country_code = models.CharField(max_length=8, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    startup_date = models.DateField(blank=True, null=True)
    investment_focus = models.CharField(max_length=255, blank=True)
    investment_range = models.CharField(max_length=255, blank=True)
    linkedin_profile = models.URLField(blank=True)
    website = models.URLField(blank=True)
    looking_for = models.TextField(blank=True)
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    is_premium = models.BooleanField(default=False)
    swipes_left = models.IntegerField(default=5)  # Daily swipes for free users
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username} ({self.get_user_type_display()})"
    
    def get_full_name(self):
        return self.user.get_full_name() or self.user.username

class Match(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    )
    
    user1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='matches_as_user1')
    user2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='matches_as_user2')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('user1', 'user2')
    
    def __str__(self):
        return f"Match between {self.user1.username} and {self.user2.username} - {self.status}"

class SwipeAction(models.Model):
    ACTION_CHOICES = (
        ('like', 'Like'),
        ('dislike', 'Dislike'),
    )
    
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='swipes_from')
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='swipes_to')
    action = models.CharField(max_length=10, choices=ACTION_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('from_user', 'to_user')
    
    def __str__(self):
        return f"{self.from_user.username} {self.action}d {self.to_user.username}"

class Waitlist(models.Model):
    email = models.EmailField(unique=True)
    user_type = models.CharField(max_length=10, choices=Profile.USER_TYPES)
    company_name = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.email} ({self.get_user_type_display()})"

# Example for your registration view (simplified)
def register(request):
    if request.method == 'POST':
        form = YourRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            profile = user.profile
            profile.user_type = form.cleaned_data['user_type']
            profile.location = form.cleaned_data['location']
            profile.country_code = form.cleaned_data['country_code']
            profile.phone = form.cleaned_data['phone']
            if profile.user_type == 'founder':
                profile.startup_date = form.cleaned_data['startup_date']
            if profile.user_type == 'investor':
                profile.investment_focus = form.cleaned_data['investment_focus']
                profile.investment_range = form.cleaned_data['investment_range']
            profile.save()
            # ...login or redirect...

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.get_or_create(user=instance)
