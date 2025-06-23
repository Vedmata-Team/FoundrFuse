from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from import_export.formats import base_formats
from .models import Profile, Match, SwipeAction, Waitlist
from core.admin import PDFExportMixin

# Profile Resource for Import/Export
class ProfileResource(resources.ModelResource):
    class Meta:
        model = Profile
        fields = (
            'id', 'user__username', 'user__email', 'user_type', 'company_name',
            'industry', 'country', 'state', 'city', 'pincode', 'location',
            'is_premium', 'swipes_left', 'created_at'
        )
        export_order = fields

@admin.register(Profile)
class ProfileAdmin(ImportExportModelAdmin, PDFExportMixin):
    resource_class = ProfileResource
    list_display = (
        'user', 'user_type', 'company_name', 'industry',
        'country', 'state', 'city', 'pincode',
        'is_premium', 'swipes_left', 'created_at'
    )
    list_filter = ('user_type', 'is_premium', 'industry', 'country', 'state', 'city')
    search_fields = (
        'user__username', 'user__email', 'company_name', 'country', 'state', 'city', 'pincode'
    )
    date_hierarchy = 'created_at'
    list_per_page = 25
    actions = ['export_as_pdf']
    formats = [base_formats.CSV, base_formats.XLSX, base_formats.JSON]
    
    fieldsets = (
        ('User Information', {
            'fields': ('user', 'user_type', 'bio', 'profile_image')
        }),
        ('Company Details', {
            'fields': ('company_name', 'industry', 'location', 'linkedin_profile', 'website')
        }),
        ('Location', {
            'fields': ('country', 'state', 'city', 'pincode')
        }),
        ('Matching Preferences', {
            'fields': ('looking_for',)
        }),
        ('Subscription Status', {
            'fields': ('is_premium', 'swipes_left')
        }),
    )

# Match Resource for Import/Export
class MatchResource(resources.ModelResource):
    class Meta:
        model = Match
        fields = ('id', 'user1__username', 'user2__username', 'status', 'created_at', 'updated_at')
        export_order = fields

@admin.register(Match)
class MatchAdmin(ImportExportModelAdmin, PDFExportMixin):
    resource_class = MatchResource
    list_display = ('user1', 'user2', 'status', 'created_at', 'updated_at')
    list_filter = ('status', 'created_at')
    search_fields = ('user1__username', 'user1__email', 'user2__username', 'user2__email')
    date_hierarchy = 'created_at'
    list_per_page = 25
    actions = ['export_as_pdf']
    formats = [base_formats.CSV, base_formats.XLSX, base_formats.JSON]

# SwipeAction Resource for Import/Export
class SwipeActionResource(resources.ModelResource):
    class Meta:
        model = SwipeAction
        fields = ('id', 'from_user__username', 'to_user__username', 'action', 'created_at')
        export_order = fields

@admin.register(SwipeAction)
class SwipeActionAdmin(ImportExportModelAdmin, PDFExportMixin):
    resource_class = SwipeActionResource
    list_display = ('from_user', 'to_user', 'action', 'created_at')
    list_filter = ('action', 'created_at')
    search_fields = ('from_user__username', 'from_user__email', 'to_user__username', 'to_user__email')
    date_hierarchy = 'created_at'
    list_per_page = 25
    actions = ['export_as_pdf']
    formats = [base_formats.CSV, base_formats.XLSX, base_formats.JSON]

# Waitlist Resource for Import/Export
class WaitlistResource(resources.ModelResource):
    class Meta:
        model = Waitlist
        fields = ('id', 'email', 'user_type', 'company_name', 'created_at')
        export_order = fields

@admin.register(Waitlist)
class WaitlistAdmin(ImportExportModelAdmin, PDFExportMixin):
    resource_class = WaitlistResource
    list_display = ('email', 'user_type', 'company_name', 'created_at')
    list_filter = ('user_type', 'created_at')
    search_fields = ('email', 'company_name')
    date_hierarchy = 'created_at'
    list_per_page = 50
    actions = ['export_as_pdf']
    formats = [base_formats.CSV, base_formats.XLSX, base_formats.JSON]
