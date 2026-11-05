from django.contrib import admin
from .models import PerformanceReport

@admin.register(PerformanceReport)
class PerformanceReportAdmin(admin.ModelAdmin):
    list_display = ['user', 'start_date', 'end_date', 'total_sessions', 'average_alignment_score', 'created_at']
    list_filter = ['created_at', 'start_date', 'end_date']
    search_fields = ['user__username', 'user__email']
    readonly_fields = ['created_at']
    
    fieldsets = (
        ('Report Information', {
            'fields': ('user', 'start_date', 'end_date')
        }),
        ('Statistics', {
            'fields': ('total_sessions', 'average_alignment_score', 'improvement_rate')
        }),
        ('Additional Data', {
            'fields': ('report_data',),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
