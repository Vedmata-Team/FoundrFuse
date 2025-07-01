from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from import_export.formats import base_formats
from .models import SubscriptionPlan, UserSubscription, PaymentHistory
from core.admin import PDFExportMixin

# SubscriptionPlan Resource for Import/Export
class SubscriptionPlanResource(resources.ModelResource):
    class Meta:
        model = SubscriptionPlan
        fields = ('id', 'name', 'description', 'price', 'duration_months', 
                 'features', 'is_active', 'created_at', 'updated_at')
        export_order = fields

@admin.register(SubscriptionPlan)
class SubscriptionPlanAdmin(ImportExportModelAdmin, PDFExportMixin):
    resource_class = SubscriptionPlanResource
    list_display = ('name', 'price', 'duration_months', 'is_active', 'created_at')
    list_filter = ('is_active', 'duration_months')
    search_fields = ('name', 'description', 'features')
    date_hierarchy = 'created_at'
    list_per_page = 15
    actions = ['export_as_pdf']
    formats = [base_formats.CSV, base_formats.XLSX, base_formats.JSON]
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'description', 'price', 'duration_months')
        }),
        ('Features and Status', {
            'fields': ('features', 'is_active')
        }),
    )

# UserSubscription Resource for Import/Export
class UserSubscriptionResource(resources.ModelResource):
    class Meta:
        model = UserSubscription
        fields = ('id', 'user__username', 'user__email', 'plan__name', 
                 'start_date', 'end_date', 'is_active', 'auto_renew',
                 'created_at', 'updated_at')
        export_order = fields

@admin.register(UserSubscription)
class UserSubscriptionAdmin(ImportExportModelAdmin, PDFExportMixin):
    resource_class = UserSubscriptionResource
    list_display = ('user', 'plan', 'start_date', 'end_date', 'is_active')  # removed 'auto_renew'
    list_filter = ('is_active', 'plan', 'start_date')  # removed 'auto_renew'
    search_fields = ('user__username', 'user__email', 'plan__name')
    date_hierarchy = 'start_date'
    list_per_page = 25
    actions = ['export_as_pdf']
    formats = [base_formats.CSV, base_formats.XLSX, base_formats.JSON]
    
    fieldsets = (
        ('User and Plan', {
            'fields': ('user', 'plan')
        }),
        ('Subscription Details', {
            'fields': ('start_date', 'end_date', 'is_active')  # removed 'auto_renew'
        }),
        ('Cancellation Details', {
            'fields': ('cancellation_date', 'cancellation_reason'),
            'classes': ('collapse',)
        }),
    )
    # Add to SubscriptionPlan model
    def features_list(self):
        return self.features.splitlines()

# PaymentHistory Resource for Import/Export
class PaymentHistoryResource(resources.ModelResource):
    class Meta:
        model = PaymentHistory
        fields = ('id', 'user__username', 'user__email', 'subscription__plan__name', 
                 'amount', 'payment_method', 'payment_id', 'status', 'payment_date')
        export_order = fields

@admin.register(PaymentHistory)
class PaymentHistoryAdmin(ImportExportModelAdmin, PDFExportMixin):
    resource_class = PaymentHistoryResource
    list_display = ('user', 'subscription', 'amount', 'payment_method', 'status', 'payment_date')
    list_filter = ('status', 'payment_method', 'payment_date')
    search_fields = ('user__username', 'user__email', 'payment_id', 'invoice_id')
    date_hierarchy = 'payment_date'
    list_per_page = 30
    actions = ['export_as_pdf']
    formats = [base_formats.CSV, base_formats.XLSX, base_formats.JSON]
    
    fieldsets = (
        ('User and Subscription', {
            'fields': ('user', 'subscription')
        }),
        ('Payment Details', {
            'fields': ('amount', 'payment_method', 'payment_id', 'invoice_id', 'status')
        }),
        ('Timestamps', {
            'fields': ('payment_date',)
        }),
    )
