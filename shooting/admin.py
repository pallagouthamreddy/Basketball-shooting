from django.contrib import admin
from .models import ShootingSession, PostureAnalysis, TrajectoryAnalysis, AIFeedback

@admin.register(ShootingSession)
class ShootingSessionAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'session_type', 'processed', 'processing_status', 'created_at']
    list_filter = ['session_type', 'processed', 'created_at']
    search_fields = ['title', 'user__username']
    readonly_fields = ['created_at', 'processing_status']
    
    fieldsets = (
        ('Session Information', {
            'fields': ('user', 'title', 'session_type', 'video', 'notes')
        }),
        ('Processing Status', {
            'fields': ('processed', 'processing_status', 'created_at')
        }),
    )

@admin.register(PostureAnalysis)
class PostureAnalysisAdmin(admin.ModelAdmin):
    list_display = ['session', 'body_alignment_score', 'elbow_angle', 'shoulder_angle', 'created_at']
    list_filter = ['created_at']
    search_fields = ['session__title', 'session__user__username']
    readonly_fields = ['created_at']

@admin.register(TrajectoryAnalysis)
class TrajectoryAnalysisAdmin(admin.ModelAdmin):
    list_display = ['session', 'predicted_success_rate', 'arc_height', 'created_at']
    readonly_fields = ['created_at']

@admin.register(AIFeedback)
class AIFeedbackAdmin(admin.ModelAdmin):
    list_display = ['session', 'feedback_type', 'priority', 'created_at']
    list_filter = ['feedback_type', 'priority', 'created_at']
    search_fields = ['session__title', 'feedback_type', 'feedback_text']
