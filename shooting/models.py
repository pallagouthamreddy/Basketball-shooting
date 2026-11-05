from django.db import models
from accounts.models import User
from django.utils import timezone

class ShootingSession(models.Model):
    SESSION_TYPE_CHOICES = (
        ('training', 'Training'),
        ('match', 'Match'),
        ('practice', 'Practice'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='shooting_sessions')
    title = models.CharField(max_length=200)
    session_type = models.CharField(max_length=20, choices=SESSION_TYPE_CHOICES, default='training')
    video = models.FileField(upload_to='shooting_videos/')
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    processed = models.BooleanField(default=False)
    processing_status = models.CharField(max_length=200, default='Pending', blank=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Shooting Session'
        verbose_name_plural = 'Shooting Sessions'
    
    def __str__(self):
        return f"{self.user.username} - {self.title}"

class PostureAnalysis(models.Model):
    session = models.OneToOneField(ShootingSession, on_delete=models.CASCADE, related_name='posture')
    elbow_angle = models.FloatField(null=True, blank=True)
    shoulder_angle = models.FloatField(null=True, blank=True)
    knee_angle = models.FloatField(null=True, blank=True)
    hip_angle = models.FloatField(null=True, blank=True)
    release_angle = models.FloatField(null=True, blank=True)
    body_alignment_score = models.FloatField(null=True, blank=True)
    posture_visualization = models.ImageField(upload_to='posture_analysis/', blank=True, null=True)
    analysis_data = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Posture Analysis'
        verbose_name_plural = 'Posture Analyses'
    
    def __str__(self):
        return f"Posture - {self.session.title}"
    
    @property
    def overall_score(self):
        return round(self.body_alignment_score, 1) if self.body_alignment_score else 0

class TrajectoryAnalysis(models.Model):
    session = models.OneToOneField(ShootingSession, on_delete=models.CASCADE, related_name='trajectory')
    ball_trajectory = models.JSONField(default=list, blank=True)
    arc_height = models.FloatField(null=True, blank=True)
    release_velocity = models.FloatField(null=True, blank=True)
    predicted_success_rate = models.FloatField(null=True, blank=True)
    trajectory_visualization = models.ImageField(upload_to='trajectory_analysis/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Trajectory Analysis'
        verbose_name_plural = 'Trajectory Analyses'
    
    def __str__(self):
        return f"Trajectory - {self.session.title}"

class AIFeedback(models.Model):
    PRIORITY_CHOICES = (
        (1, 'Low'),
        (2, 'Medium'),
        (3, 'High'),
    )
    
    session = models.ForeignKey(ShootingSession, on_delete=models.CASCADE, related_name='feedbacks')
    feedback_type = models.CharField(max_length=50)
    feedback_text = models.TextField()
    correction_suggestion = models.TextField()
    priority = models.IntegerField(choices=PRIORITY_CHOICES, default=2)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-priority', '-created_at']
        verbose_name = 'AI Feedback'
        verbose_name_plural = 'AI Feedbacks'
    
    def __str__(self):
        return f"{self.feedback_type} - {self.session.title}"
    
    def get_priority_class(self):
        if self.priority == 3:
            return 'warning'
        elif self.priority == 2:
            return 'info'
        return 'success'
