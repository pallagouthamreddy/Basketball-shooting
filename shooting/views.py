from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from .models import ShootingSession, PostureAnalysis, TrajectoryAnalysis, AIFeedback
from .forms import VideoUploadForm
from .pose_analyzer import PoseAnalyzer
import traceback

@login_required
def upload_video(request):
    """Handle video upload and trigger AI analysis"""
    if request.method == 'POST':
        form = VideoUploadForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                with transaction.atomic():
                    # Save session
                    session = form.save(commit=False)
                    session.user = request.user
                    session.processing_status = 'Processing...'
                    session.save()
                    
                    messages.success(request, '✅ Video uploaded successfully! AI analysis in progress...')
                    
                    # Process video with AI
                    try:
                        analyzer = PoseAnalyzer()
                        video_path = session.video.path
                        
                        # Update status
                        session.processing_status = 'Analyzing pose...'
                        session.save()
                        
                        # Run analysis
                        analysis_result = analyzer.analyze_video(video_path)
                        
                        # Save posture analysis
                        posture = PostureAnalysis.objects.create(
                            session=session,
                            elbow_angle=analysis_result['elbow_angle'],
                            shoulder_angle=analysis_result['shoulder_angle'],
                            knee_angle=analysis_result['knee_angle'],
                            hip_angle=analysis_result.get('hip_angle', 0),
                            release_angle=analysis_result['release_angle'],
                            body_alignment_score=analysis_result['body_alignment_score'],
                            analysis_data=analysis_result
                        )
                        
                        # Save trajectory analysis (with predicted success rate)
                        success_rate = min(analysis_result['body_alignment_score'] + 10, 95)
                        trajectory = TrajectoryAnalysis.objects.create(
                            session=session,
                            predicted_success_rate=success_rate,
                            arc_height=45.0,  # Default value
                            release_velocity=7.5  # Default value
                        )
                        
                        # Generate and save AI feedback
                        feedbacks = analyzer.generate_feedback(analysis_result)
                        for fb in feedbacks:
                            AIFeedback.objects.create(
                                session=session,
                                feedback_type=fb['type'],
                                feedback_text=fb['text'],
                                correction_suggestion=fb['suggestion'],
                                priority=fb['priority']
                            )
                        
                        # Mark as processed
                        session.processed = True
                        session.processing_status = 'Completed'
                        session.save()
                        
                        messages.success(request, '🎯 Analysis completed successfully!')
                        
                    except Exception as e:
                        session.processing_status = f'Error: {str(e)}'
                        session.save()
                        messages.error(request, f'❌ Analysis failed: {str(e)}')
                        print(f"Analysis Error: {traceback.format_exc()}")
                    
                    return redirect('shooting:session_detail', pk=session.pk)
                    
            except Exception as e:
                messages.error(request, f'Error uploading video: {str(e)}')
                print(f"Upload Error: {traceback.format_exc()}")
        else:
            messages.error(request, 'Please correct the errors in the form.')
    else:
        form = VideoUploadForm()
    
    return render(request, 'shooting/upload.html', {'form': form})

@login_required
def session_list(request):
    """Display list of all user sessions"""
    sessions = ShootingSession.objects.filter(user=request.user).select_related('posture', 'trajectory')
    
    context = {
        'sessions': sessions,
        'total_sessions': sessions.count(),
        'processed_sessions': sessions.filter(processed=True).count()
    }
    
    return render(request, 'shooting/session_list.html', context)

@login_required
def session_detail(request, pk):
    """Display detailed analysis for a specific session"""
    session = get_object_or_404(ShootingSession, pk=pk, user=request.user)
    
    # Get related analysis data
    posture = getattr(session, 'posture', None)
    trajectory = getattr(session, 'trajectory', None)
    feedbacks = session.feedbacks.all().order_by('-priority', 'id')
    
    context = {
        'session': session,
        'posture': posture,
        'trajectory': trajectory,
        'feedbacks': feedbacks,
    }
    
    return render(request, 'shooting/session_detail.html', context)

@login_required
def delete_session(request, pk):
    """Delete a shooting session"""
    session = get_object_or_404(ShootingSession, pk=pk, user=request.user)
    
    if request.method == 'POST':
        title = session.title
        session.delete()
        messages.success(request, f'Session "{title}" deleted successfully.')
        return redirect('shooting:session_list')
    
    return render(request, 'shooting/session_confirm_delete.html', {'session': session})
