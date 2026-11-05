"""
Enhanced Sample Data Generator for Basketball Analysis System
Creates realistic test data with proper relationships
"""

import os
import django
import random
from datetime import datetime, timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from accounts.models import User
from shooting.models import ShootingSession, PostureAnalysis, TrajectoryAnalysis, AIFeedback

class DataGenerator:
    """Generate comprehensive sample data"""
    
    def __init__(self):
        self.session_titles = [
            "Free Throw Practice",
            "3-Point Shooting Drill",
            "Mid-Range Shots",
            "Game Situation Practice",
            "Morning Workout Session",
            "Evening Training",
            "Competition Preparation",
            "Technique Refinement",
            "Power Shooting Drill",
            "Accuracy Training"
        ]
        
        self.feedback_templates = {
            'excellent': {
                'type': 'Excellent Form',
                'text': 'Your shooting mechanics are outstanding!',
                'suggestion': 'Maintain this consistency. Focus on mental preparation.',
                'priority': 1
            },
            'good': {
                'type': 'Good Technique',
                'text': 'Your form is solid with minor improvements possible.',
                'suggestion': 'Work on maintaining balance throughout the shot.',
                'priority': 2
            },
            'needs_work': {
                'type': 'Form Improvement Needed',
                'text': 'Your shooting form requires attention.',
                'suggestion': 'Focus on proper elbow alignment and follow-through.',
                'priority': 3
            }
        }
    
    def create_users(self, count=5):
        """Create sample users"""
        print(f"Creating {count} sample users...")
        users = []
        
        for i in range(1, count + 1):
            username = f'player{i}'
            
            # Skip if user exists
            if User.objects.filter(username=username).exists():
                print(f"  ⚠ User {username} already exists, skipping...")
                users.append(User.objects.get(username=username))
                continue
            
            user = User.objects.create_user(
                username=username,
                email=f'player{i}@basketball.com',
                password='password123',
                user_type='player',
                first_name=f'Player',
                last_name=f'{i}',
                phone=f'+91 98765{43210 + i}',
                height=round(random.uniform(175, 200), 2),
                weight=round(random.uniform(70, 95), 2)
            )
            users.append(user)
            print(f"  ✓ Created: {username} (password: password123)")
        
        # Create a coach
        if not User.objects.filter(username='coach1').exists():
            coach = User.objects.create_user(
                username='coach1',
                email='coach@basketball.com',
                password='password123',
                user_type='coach',
                first_name='John',
                last_name='Coach'
            )
            print(f"  ✓ Created: coach1 (password: password123)")
        
        return users
    
    def create_sessions_for_user(self, user, count=5):
        """Create sessions with realistic progression"""
        print(f"\nCreating {count} sessions for {user.username}...")
        
        base_score = random.uniform(65, 75)  # Starting skill level
        
        for i in range(count):
            # Simulate skill progression
            days_ago = count - i
            created_date = datetime.now() - timedelta(days=days_ago * 2)
            
            # Gradual improvement over time
            score_variation = random.uniform(-5, 10)
            alignment_score = min(95, base_score + (i * 2) + score_variation)
            
            session = ShootingSession.objects.create(
                user=user,
                title=f"{random.choice(self.session_titles)} - Session {i+1}",
                session_type=random.choice(['training', 'practice', 'match']),
                notes=f"Session notes for {user.username}",
                created_at=created_date,
                processed=True,
                processing_status='Completed'
            )
            
            # Generate realistic angles
            elbow = round(random.uniform(85, 105), 2)
            shoulder = round(random.uniform(125, 145), 2)
            knee = round(random.uniform(150, 170), 2)
            hip = round(random.uniform(170, 180), 2)
            release = round(random.uniform(45, 55), 2)
            
            # Create posture analysis
            posture = PostureAnalysis.objects.create(
                session=session,
                elbow_angle=elbow,
                shoulder_angle=shoulder,
                knee_angle=knee,
                hip_angle=hip,
                release_angle=release,
                body_alignment_score=round(alignment_score, 2),
                analysis_data={
                    'frames_processed': random.randint(50, 150),
                    'total_frames': random.randint(200, 500)
                }
            )
            
            # Create trajectory analysis
            success_rate = min(95, alignment_score + random.uniform(-3, 8))
            trajectory = TrajectoryAnalysis.objects.create(
                session=session,
                predicted_success_rate=round(success_rate, 2),
                arc_height=round(random.uniform(40, 50), 2),
                release_velocity=round(random.uniform(6.5, 8.5), 2)
            )
            
            # Generate appropriate feedback
            if alignment_score >= 85:
                feedback_key = 'excellent'
            elif alignment_score >= 75:
                feedback_key = 'good'
            else:
                feedback_key = 'needs_work'
            
            template = self.feedback_templates[feedback_key]
            
            AIFeedback.objects.create(
                session=session,
                feedback_type=template['type'],
                feedback_text=template['text'],
                correction_suggestion=template['suggestion'],
                priority=template['priority']
            )
            
            # Add specific angle feedback
            if elbow < 85 or elbow > 105:
                AIFeedback.objects.create(
                    session=session,
                    feedback_type='Elbow Position',
                    feedback_text=f'Your elbow angle ({elbow:.1f}°) is outside optimal range.',
                    correction_suggestion='Adjust elbow to 90-100 degrees for better control.',
                    priority=3
                )
            
            print(f"  ✓ Session {i+1}: {session.title} (Score: {alignment_score:.1f}%)")
    
    def generate_all(self, user_count=5, sessions_per_user=5):
        """Generate complete dataset"""
        print("=" * 60)
        print("Basketball AI - Sample Data Generator")
        print("=" * 60)
        
        users = self.create_users(user_count)
        
        for user in users:
            if user.user_type == 'player':
                self.create_sessions_for_user(user, sessions_per_user)
        
        print("\n" + "=" * 60)
        print("✓ Sample data generation complete!")
        print("=" * 60)
        print(f"\nTotal Users Created: {len(users)}")
        print(f"Total Sessions: {ShootingSession.objects.count()}")
        print(f"Total Analyses: {PostureAnalysis.objects.count()}")
        print("\nLogin Credentials:")
        print("  Username: player1-5 | Password: password123")
        print("  Username: coach1    | Password: password123")
        print("=" * 60)

if __name__ == '__main__':
    generator = DataGenerator()
    generator.generate_all(user_count=5, sessions_per_user=7)
