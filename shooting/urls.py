from django.urls import path
from . import views

app_name = 'shooting'

urlpatterns = [
    path('upload/', views.upload_video, name='upload'),
    path('sessions/', views.session_list, name='session_list'),
    path('session/<int:pk>/', views.session_detail, name='session_detail'),
    path('session/<int:pk>/delete/', views.delete_session, name='delete_session'),
]
