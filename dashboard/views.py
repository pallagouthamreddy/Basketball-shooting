from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from accounts.models import User
from shooting.models import ShootingSession, PostureAnalysis
from django.db.models import Count, Avg, Q
from datetime import datetime, timedelta

@login_required
def home(request):
    """Route to appropriate dashboard based on user type"""
    if request.user.user_type == 'admin' or request.user.is_staff:
        return redirect('dashboard:admin')
    else:
        return user_dashboard(request)

@login_required
def user_dashboard(request):
    """User dashboard with personal statistics"""
    user = request.user
    
    # Get user's sessions
    all_sessions = ShootingSession.objects.filter(user=user)
    processed_sessions = all_sessions.filter(processed=True)
    
    # Recent sessions
    recent_sessions = all_sessions.order_by('-created_at')[:5]
    
    # Calculate statistics
    total_sessions = all_sessions.count()
    processed_count = processed_sessions.count()
    
    # Average alignment score
    avg_score = PostureAnalysis.objects.filter(
        session__user=user
    ).aggregate(Avg('body_alignment_score'))['body_alignment_score__avg'] or 0
    
    # Get latest analysis
    latest_session = processed_sessions.first()
    latest_posture = None
    if latest_session and hasattr(latest_session, 'posture'):
        latest_posture = latest_session.posture
    
    context = {
        'user': user,
        'total_sessions': total_sessions,
        'processed_sessions': processed_count,
        'pending_sessions': total_sessions - processed_count,
        'avg_score': round(avg_score, 1),
        'recent_sessions': recent_sessions,
        'latest_posture': latest_posture,
        'latest_session': latest_session,
    }
    
    return render(request, 'dashboard/user_dashboard.html', context)

@staff_member_required
def admin_dashboard(request):
    """Admin dashboard with system-wide statistics"""
    
    # User statistics
    total_users = User.objects.filter(user_type='player').count()
    total_coaches = User.objects.filter(user_type='coach').count()
    new_users_today = User.objects.filter(
        created_at__date=datetime.now().date()
    ).count()
    
    # Session statistics
    total_sessions = ShootingSession.objects.count()
    processed_sessions = ShootingSession.objects.filter(processed=True).count()
    pending_sessions = total_sessions - processed_sessions
    
    # Performance statistics
    avg_system_score = PostureAnalysis.objects.aggregate(
        Avg('body_alignment_score')
    )['body_alignment_score__avg'] or 0
    
    # Recent activity
    recent_users = User.objects.all().order_by('-created_at')[:5]
    recent_sessions = ShootingSession.objects.select_related('user').order_by('-created_at')[:10]
    
    # Session type distribution
    session_types = ShootingSession.objects.values('session_type').annotate(
        count=Count('id')
    )
    
    context = {
        'total_users': total_users,
        'total_coaches': total_coaches,
        'new_users_today': new_users_today,
        'total_sessions': total_sessions,
        'processed_sessions': processed_sessions,
        'pending_sessions': pending_sessions,
        'avg_system_score': round(avg_system_score, 1),
        'recent_users': recent_users,
        'recent_sessions': recent_sessions,
        'session_types': session_types,
    }
    
    return render(request, 'dashboard/admin_dashboard.html', context)
