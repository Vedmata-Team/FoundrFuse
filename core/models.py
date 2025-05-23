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
