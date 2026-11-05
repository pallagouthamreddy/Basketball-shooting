from django.contrib import admin
from .models import MLModel, TrainingDataset

@admin.register(MLModel)
class MLModelAdmin(admin.ModelAdmin):
    list_display = ['name', 'model_type', 'version', 'accuracy', 'is_active', 'created_at']
    list_filter = ['model_type', 'is_active', 'created_at']
    search_fields = ['name', 'version', 'description']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Model Information', {
            'fields': ('name', 'model_type', 'version', 'description')
        }),
        ('Model File & Performance', {
            'fields': ('model_file', 'accuracy', 'is_active')
        }),
        ('Parameters', {
            'fields': ('parameters',),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(TrainingDataset)
class TrainingDatasetAdmin(admin.ModelAdmin):
    list_display = ['name', 'dataset_type', 'size', 'created_at']
    list_filter = ['dataset_type', 'created_at']
    search_fields = ['name', 'description']
    readonly_fields = ['created_at']
