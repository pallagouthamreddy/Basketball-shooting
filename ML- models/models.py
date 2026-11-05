from django.db import models

class MLModel(models.Model):
    MODEL_TYPE_CHOICES = (
        ('pose_detection', 'Pose Detection'),
        ('trajectory_prediction', 'Trajectory Prediction'),
        ('success_prediction', 'Success Prediction'),
    )
    
    name = models.CharField(max_length=200)
    model_type = models.CharField(max_length=50, choices=MODEL_TYPE_CHOICES)
    version = models.CharField(max_length=50)
    model_file = models.FileField(upload_to='ml_models/', blank=True, null=True)
    accuracy = models.FloatField(null=True, blank=True)
    is_active = models.BooleanField(default=False)
    description = models.TextField(blank=True)
    parameters = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'ML Model'
        verbose_name_plural = 'ML Models'
    
    def __str__(self):
        return f"{self.name} v{self.version}"

class TrainingDataset(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    dataset_file = models.FileField(upload_to='datasets/')
    size = models.IntegerField(help_text="Number of samples")
    dataset_type = models.CharField(max_length=50, default='pose')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Training Dataset'
        verbose_name_plural = 'Training Datasets'
    
    def __str__(self):
        return self.name
