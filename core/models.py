from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.urls import reverse

class Industry(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    
    class Meta:
        verbose_name_plural = 'Industries'
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    
    class Meta:
        verbose_name_plural = 'Categories'
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class Blog(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    industry = models.ForeignKey(Industry, on_delete=models.SET_NULL, null=True, blank=True, related_name='blogs')
    categories = models.ManyToManyField(Category, related_name='blogs')
    featured_image = models.ImageField(upload_to='blog_images/')
    summary = models.TextField()
    content = models.TextField()
    views_count = models.PositiveIntegerField(default=0)
    is_featured = models.BooleanField(default=False)
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('core:blog_detail', kwargs={'slug': self.slug})
    
    def increment_views(self):
        self.views_count += 1
        self.save()

class NewsletterSubscriber(models.Model):
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.email

class SiteSettings(models.Model):
    # General Site Information
    site_name = models.CharField(max_length=100, default='FoundrFuse')
    tagline = models.CharField(max_length=200, default='Empowering Ideas, One Match at a Time')
    about_description = models.TextField(blank=True, help_text="Brief description about the platform")
    logo = models.ImageField(upload_to='site/', blank=True, null=True)
    favicon = models.ImageField(upload_to='site/', blank=True, null=True)
    
    # Contact Information
    contact_email = models.EmailField(blank=True)
    support_email = models.EmailField(blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    
    # Social Media Links
    twitter_url = models.URLField(blank=True)
    facebook_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)
    instagram_url = models.URLField(blank=True)
    youtube_url = models.URLField(blank=True)
    
    # Footer Settings
    footer_text = models.CharField(max_length=200, blank=True)
    copyright_text = models.CharField(max_length=200, blank=True, default="© 2025 FoundrFuse. All rights reserved.")
    
    # Platform Settings
    max_free_swipes = models.PositiveIntegerField(default=5, help_text="Number of daily swipes for free users")
    maintenance_mode = models.BooleanField(default=False, help_text="Set to True to put the site in maintenance mode")
    maintenance_message = models.TextField(blank=True, default="We're improving FoundrFuse! We'll be back shortly.")
    
    # SEO Settings
    meta_description = models.TextField(blank=True, help_text="Default meta description for SEO")
    meta_keywords = models.TextField(blank=True, help_text="Default meta keywords for SEO, comma separated")
    google_analytics_id = models.CharField(max_length=50, blank=True)
    
    # Privacy and Legal
    privacy_policy = models.TextField(blank=True)
    terms_of_service = models.TextField(blank=True)
    cookie_policy = models.TextField(blank=True)
    
    # System Settings
    registration_enabled = models.BooleanField(default=True, help_text="Allow new user registration")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Site Settings'
        verbose_name_plural = 'Site Settings'
    
    def __str__(self):
        return self.site_name
        
    def save(self, *args, **kwargs):
        # Ensure there's only ever one instance of SiteSettings
        if not self.pk and SiteSettings.objects.exists():
            # Update existing settings instead of creating a new one
            self.pk = SiteSettings.objects.first().pk
        return super().save(*args, **kwargs)

class Testimonial(models.Model):
    USER_TYPE_CHOICES = (
        ('founder', 'Founder'),
        ('investor', 'Investor'),
    )
    name = models.CharField(
        max_length=100,
        help_text="Full name of the person giving the testimonial."
    )
    role = models.CharField(
        max_length=100,
        blank=True,
        help_text="Their role or title (e.g., CEO, Angel Investor)."
    )
    company = models.CharField(
        max_length=100,
        blank=True,
        help_text="Their company or organization (optional)."
    )
    text = models.TextField(
        help_text="The testimonial text (what the user says about FoundrFuse)."
    )
    user_type = models.CharField(
        max_length=10,
        choices=USER_TYPE_CHOICES,
        help_text="Is this testimonial from a Founder or an Investor?"
    )
    category = models.CharField(
        max_length=100,
        blank=True,
        help_text="Industry or category (e.g., Tech, Healthcare)."
    )
    date = models.DateField(
        help_text="Date when the testimonial was given."
    )
    avatar = models.ImageField(
        upload_to='testimonials/',
        blank=True,
        null=True,
        help_text="Optional: Upload a profile photo for this testimonial."
    )

    class Meta:
        ordering = ['-date']
        verbose_name = "Testimonial"
        verbose_name_plural = "Testimonials"

    def __str__(self):
        return f"{self.name} ({self.get_user_type_display()})"

class FeatureFAQ(models.Model):
    question = models.CharField(max_length=255, help_text="FAQ question for the Feature page.")
    answer = models.TextField(help_text="Answer to the FAQ question.")
    order = models.PositiveIntegerField(default=0, help_text="Order of appearance on the Feature page.")

    class Meta:
        verbose_name = "Feature Page FAQ"
        verbose_name_plural = "Feature Page FAQs"
        ordering = ['order']

    def __str__(self):
        return self.question




class FounderSuccessStory(models.Model):
    name = models.CharField(max_length=100, help_text="Name of the founder.")
    role = models.CharField(max_length=100, blank=True, help_text="Role or title (e.g., Founder & CEO).")
    company = models.CharField(max_length=100, blank=True, help_text="Company or startup name.")
    quote = models.TextField(help_text="Success story or testimonial quote.")
    avatar = models.ImageField(upload_to='success_stories/', blank=True, null=True, help_text="Photo of the founder.")
    order = models.PositiveIntegerField(default=0, help_text="Display order.")

    class Meta:
        verbose_name = "Founder Success Story"
        verbose_name_plural = "Founder Success Stories"
        ordering = ['order']

    def __str__(self):
        return f"{self.name} ({self.company})"


class FounderFAQ(models.Model):
    question = models.CharField(max_length=255, help_text="FAQ question for the Founders page.")
    answer = models.TextField(help_text="Answer to the FAQ question.")
    order = models.PositiveIntegerField(default=0, help_text="Order of appearance on the Founders page.")

    class Meta:
        verbose_name = "Founder Page FAQ"
        verbose_name_plural = "Founder Page FAQs"
        ordering = ['order']

    def __str__(self):
        return self.question