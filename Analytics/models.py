from django.db import models
from accounts.models import User

class PerformanceReport(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reports')
    start_date = models.DateField()
    end_date = models.DateField()
    total_sessions = models.IntegerField(default=0)
    average_alignment_score = models.FloatField(default=0.0)
    improvement_rate = models.FloatField(default=0.0)
    report_data = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Performance Report'
        verbose_name_plural = 'Performance Reports'
    
    def __str__(self):
        return f"{self.user.username} - Report ({self.start_date} to {self.end_date})"
