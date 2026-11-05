from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from shooting.models import ShootingSession, PostureAnalysis
from django.db.models import Avg, Count, Max, Min
from datetime import datetime, timedelta
import json

@login_required
def performance_dashboard(request):
    """Main analytics dashboard with performance metrics"""
    user = request.user
    
    # Get sessions from last 30 days
    thirty_days_ago = datetime.now() - timedelta(days=30)
    recent_sessions = ShootingSession.objects.filter(
        user=user,
        created_at__gte=thirty_days_ago,
        processed=True
    ).select_related('posture', 'trajectory')
    
    # Calculate statistics
    total_sessions = recent_sessions.count()
    
    posture_analyses = PostureAnalysis.objects.filter(
        session__in=recent_sessions
    )
    
    stats = posture_analyses.aggregate(
        avg_alignment=Avg('body_alignment_score'),
        avg_elbow=Avg('elbow_angle'),
        avg_shoulder=Avg('shoulder_angle'),
        avg_knee=Avg('knee_angle'),
        max_score=Max('body_alignment_score'),
        min_score=Min('body_alignment_score')
    )
    
    # Get trend data for chart
    trend_data = []
    for session in recent_sessions.order_by('created_at'):
        if hasattr(session, 'posture'):
            trend_data.append({
                'date': session.created_at.strftime('%Y-%m-%d'),
                'title': session.title,
                'score': round(session.posture.body_alignment_score, 1)
            })
    
    context = {
        'total_sessions': total_sessions,
        'avg_alignment': round(stats['avg_alignment'] or 0, 1),
        'avg_elbow': round(stats['avg_elbow'] or 0, 1),
        'avg_shoulder': round(stats['avg_shoulder'] or 0, 1),
        'max_score': round(stats['max_score'] or 0, 1),
        'min_score': round(stats['min_score'] or 0, 1),
        'trend_data': json.dumps(trend_data),
        'recent_sessions': recent_sessions[:5]
    }
    
    return render(request, 'analytics/dashboard.html', context)

@login_required
def progress_tracking(request):
    """Detailed progress tracking over time"""
    user = request.user
    sessions = ShootingSession.objects.filter(
        user=user, 
        processed=True
    ).select_related('posture', 'trajectory').order_by('created_at')
    
    progress_data = []
    for session in sessions:
        if hasattr(session, 'posture'):
            progress_data.append({
                'session': session,
                'posture': session.posture,
                'trajectory': getattr(session, 'trajectory', None)
            })
    
    return render(request, 'analytics/progress.html', {
        'progress_data': progress_data,
        'total_sessions': len(progress_data)
    })
