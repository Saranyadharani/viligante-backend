from django.contrib import admin
from .models import ScanResult, SecurityReport, CommunityReport, CommunityStory

@admin.register(ScanResult)
class ScanResultAdmin(admin.ModelAdmin):
    list_display = ['url', 'domain', 'risk_level', 'risk_category', 'ssl_grade', 'domain_age', 'created_at']
    list_filter = ['risk_category', 'ssl_grade', 'created_at']
    search_fields = ['url', 'domain']
    ordering = ['-created_at']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(SecurityReport)
class SecurityReportAdmin(admin.ModelAdmin):
    list_display = ['scan_result', 'created_at']
    list_filter = ['created_at']

@admin.register(CommunityReport)
class CommunityReportAdmin(admin.ModelAdmin):
    list_display = ['scan_result', 'user', 'accurate', 'created_at']
    list_filter = ['accurate', 'created_at']

@admin.register(CommunityStory)
class CommunityStoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'scam_type', 'status', 'is_public', 'created_at']
    list_filter = ['scam_type', 'status', 'is_public', 'created_at']
    search_fields = ['title', 'story']