from django.contrib import admin
from django.http import HttpResponse
from django.urls import path
from django.template.loader import render_to_string
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from import_export.formats import base_formats
from xhtml2pdf import pisa
from io import BytesIO
from .models import Industry, Category, Blog, NewsletterSubscriber, SiteSettings, Testimonial, FeatureFAQ, ChatbotFAQ

# Base PDF export mixin
class PDFExportMixin:
    def export_as_pdf(self, request, queryset):
        # Get model name for the template and filename
        model_name = queryset.model._meta.verbose_name_plural
        
        # Prepare context for the template
        context = {
            'title': f'{model_name.title()} Export',
            'objects': queryset,
            'headers': [field.verbose_name.title() for field in queryset.model._meta.fields],
            'fields': [field.name for field in queryset.model._meta.fields]
        }
        
        # Render the HTML template
        html_string = render_to_string('admin/pdf_export_template.html', context)
        
        # Create a file-like buffer to receive PDF data
        buffer = BytesIO()
        
        # Convert HTML to PDF
        pisa_status = pisa.CreatePDF(html_string, dest=buffer)
        
        # If the conversion was successful
        if not pisa_status.err:
            # FileResponse sets the Content-Disposition header so that browsers
            # present the option to save the file
            buffer.seek(0)
            response = HttpResponse(buffer.read(), content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="{model_name}.pdf"'
            return response
        
        return HttpResponse("Error generating PDF", content_type='text/plain')
    
    export_as_pdf.short_description = "Export selected items as PDF"

# Industry Resource for Import/Export
class IndustryResource(resources.ModelResource):
    class Meta:
        model = Industry
        fields = ('id', 'name', 'slug')
        export_order = fields

@admin.register(Industry)
class IndustryAdmin(ImportExportModelAdmin, PDFExportMixin):
    resource_class = IndustryResource
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'slug')
    list_per_page = 25
    actions = ['export_as_pdf']
    formats = [base_formats.CSV, base_formats.XLSX, base_formats.JSON]

# Category Resource for Import/Export
class CategoryResource(resources.ModelResource):
    class Meta:
        model = Category
        fields = ('id', 'name', 'slug')
        export_order = fields

@admin.register(Category)
class CategoryAdmin(ImportExportModelAdmin, PDFExportMixin):
    resource_class = CategoryResource
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'slug')
    list_per_page = 25
    actions = ['export_as_pdf']
    formats = [base_formats.CSV, base_formats.XLSX, base_formats.JSON]

# Blog Resource for Import/Export
class BlogResource(resources.ModelResource):
    class Meta:
        model = Blog
        fields = ('id', 'title', 'slug', 'author__username', 'industry__name', 'summary', 
                 'views_count', 'is_featured', 'is_published', 'created_at', 'updated_at')
        export_order = fields

@admin.register(Blog)
class BlogAdmin(ImportExportModelAdmin, PDFExportMixin):
    resource_class = BlogResource
    list_display = ('title', 'author', 'industry', 'created_at', 'views_count', 'is_featured', 'is_published')
    list_filter = ('is_featured', 'is_published', 'created_at', 'industry', 'categories')
    search_fields = ('title', 'summary', 'content', 'author__username')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'created_at'
    filter_horizontal = ('categories',)
    list_per_page = 25
    actions = ['export_as_pdf']
    formats = [base_formats.CSV, base_formats.XLSX, base_formats.JSON]
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'author', 'summary', 'content')
        }),
        ('Categorization', {
            'fields': ('industry', 'categories')
        }),
        ('Media', {
            'fields': ('featured_image',)
        }),
        ('Publishing Options', {
            'fields': ('is_featured', 'is_published')
        }),
        ('Statistics', {
            'fields': ('views_count',),
            'classes': ('collapse',)
        }),
    )

# Newsletter Subscriber Resource for Import/Export
class NewsletterSubscriberResource(resources.ModelResource):
    class Meta:
        model = NewsletterSubscriber
        fields = ('id', 'email', 'created_at')
        export_order = fields

@admin.register(NewsletterSubscriber)
class NewsletterSubscriberAdmin(ImportExportModelAdmin, PDFExportMixin):
    resource_class = NewsletterSubscriberResource
    list_display = ('email', 'created_at')
    search_fields = ('email',)
    date_hierarchy = 'created_at'
    list_per_page = 50
    actions = ['export_as_pdf']
    formats = [base_formats.CSV, base_formats.XLSX, base_formats.JSON]

# Site Settings Resource for Import/Export
class SiteSettingsResource(resources.ModelResource):
    class Meta:
        model = SiteSettings
        exclude = ('privacy_policy', 'terms_of_service', 'cookie_policy', 'about_description')

@admin.register(SiteSettings)
class SiteSettingsAdmin(ImportExportModelAdmin):
    resource_class = SiteSettingsResource
    
    fieldsets = (
        ('General Information', {
            'fields': ('site_name', 'tagline', 'about_description', 'logo', 'favicon')
        }),
        ('Contact Information', {
            'fields': ('contact_email', 'support_email', 'phone_number', 'address')
        }),
        ('Social Media', {
            'fields': ('twitter_url', 'facebook_url', 'linkedin_url', 'instagram_url', 'youtube_url')
        }),
        ('Footer', {
            'fields': ('footer_text', 'copyright_text')
        }),
        ('Platform Settings', {
            'fields': ('max_free_swipes', 'maintenance_mode', 'maintenance_message')
        }),
        ('SEO Settings', {
            'fields': ('meta_description', 'meta_keywords', 'google_analytics_id'),
            'classes': ('collapse',)
        }),
        ('Legal Documents', {
            'fields': ('privacy_policy', 'terms_of_service', 'cookie_policy'),
            'classes': ('collapse',)
        }),
        ('System Settings', {
            'fields': ('registration_enabled',),
            'classes': ('collapse',)
        }),
    )
    
    def has_add_permission(self, request):
        # Only allow one site settings instance
        return not SiteSettings.objects.exists()

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('name', 'user_type', 'role', 'company', 'category', 'date')
    list_filter = ('user_type', 'category', 'date')
    search_fields = ('name', 'role', 'company', 'category', 'text')
    fieldsets = (
        (None, {
            'fields': (
                'name',
                'role',
                'company',
                'user_type',
                'category',
                'date',
                'avatar',
                'text',
            ),
            'description': (
                "<b>Tips:</b> <ul>"
                "<li><b>Name</b>: Full name of the testimonial giver.</li>"
                "<li><b>User Type</b>: Choose Founder or Investor. This controls which section the testimonial appears in.</li>"
                "<li><b>Category</b>: Industry or area (e.g., Tech, Healthcare).</li>"
                "<li><b>Date</b>: When the testimonial was given.</li>"
                "<li><b>Avatar</b>: Optional profile image.</li>"
                "<li><b>Text</b>: The testimonial itself.</li>"
                "</ul>"
            )
        }),
    )

@admin.register(FeatureFAQ)
class FeatureFAQAdmin(admin.ModelAdmin):
    list_display = ('question', 'order')
    search_fields = ('question', 'answer')
    ordering = ('order',)
    fieldsets = (
        (None, {
            'fields': ('question', 'answer', 'order'),
            'description': (
                "<b>Note:</b> These FAQs will appear on the <b>Feature Page</b> under the FAQ section."
            )
        }),
    )
    
    
from .models import FounderSuccessStory, FounderFAQ

@admin.register(FounderSuccessStory)
class FounderSuccessStoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'company', 'role', 'order')
    search_fields = ('name', 'company', 'role', 'quote')
    ordering = ('order',)
    fieldsets = (
        (None, {
            'fields': ('name', 'role', 'company', 'quote', 'avatar', 'order'),
            'description': (
                "<b>Note:</b> These success stories will appear on the <b>Founders Page</b> in the Success Stories section."
            )
        }),
    )

@admin.register(FounderFAQ)
class FounderFAQAdmin(admin.ModelAdmin):
    list_display = ('question', 'order')
    search_fields = ('question', 'answer')
    ordering = ('order',)
    fieldsets = (
        (None, {
            'fields': ('question', 'answer', 'order'),
            'description': (
                "<b>Note:</b> These FAQs will appear on the <b>Founders Page</b> under the FAQ section."
            )
        }),
    )

@admin.register(ChatbotFAQ)
class ChatbotFAQAdmin(admin.ModelAdmin):
    list_display = ('question',)
    search_fields = ('question', 'answer')
