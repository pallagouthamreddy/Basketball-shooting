from django.urls import path
from . import views

app_name = 'analytics'

urlpatterns = [
    path('dashboard/', views.performance_dashboard, name='dashboard'),
    path('progress/', views.progress_tracking, name='progress'),
]
