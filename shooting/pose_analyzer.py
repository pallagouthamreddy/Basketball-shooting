import cv2
import mediapipe as mp
import numpy as np
import math
import os
from django.conf import settings

class PoseAnalyzer:
    """
    Complete AI-powered pose analysis engine using MediaPipe
    Analyzes basketball shooting form and provides detailed feedback
    """
    
    def __init__(self):
        self.mp_pose = mp.solutions.pose
        self.mp_draw = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles
        self.pose = self.mp_pose.Pose(
            static_image_mode=False,
            model_complexity=2,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
    
    def calculate_angle(self, a, b, c):
        """Calculate angle between three points in 3D space"""
        a = np.array(a)
        b = np.array(b)
        c = np.array(c)
        
        radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
        angle = np.abs(radians * 180.0 / np.pi)
        
        if angle > 180.0:
            angle = 360 - angle
            
        return angle
    
    def get_landmark_coords(self, landmarks, idx):
        """Extract x, y coordinates from landmark"""
        return [landmarks[idx].x, landmarks[idx].y]
    
    def analyze_video(self, video_path):
        """
        Main analysis function - processes video and extracts pose data
        Returns comprehensive analysis results
        """
        if not os.path.exists(video_path):
            raise FileNotFoundError(f"Video file not found: {video_path}")
        
        cap = cv2.VideoCapture(video_path)
        
        if not cap.isOpened():
            raise ValueError("Cannot open video file")
        
        angles_data = {
            'elbow': [],
            'shoulder': [],
            'knee': [],
            'hip': [],
            'release': []
        }
        
        frame_count = 0
        processed_frames = 0
        
        try:
            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break
                
                frame_count += 1
                
                # Process every 5th frame for efficiency
                if frame_count % 5 != 0:
                    continue
                
                # Convert BGR to RGB
                image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                results = self.pose.process(image_rgb)
                
                if results.pose_landmarks:
                    landmarks = results.pose_landmarks.landmark
                    processed_frames += 1
                    
                    # Right arm analysis (shooting arm)
                    try:
                        # Shoulder-Elbow-Wrist angle (Elbow angle)
                        shoulder = self.get_landmark_coords(landmarks, self.mp_pose.PoseLandmark.RIGHT_SHOULDER.value)
                        elbow = self.get_landmark_coords(landmarks, self.mp_pose.PoseLandmark.RIGHT_ELBOW.value)
                        wrist = self.get_landmark_coords(landmarks, self.mp_pose.PoseLandmark.RIGHT_WRIST.value)
                        
                        elbow_angle = self.calculate_angle(shoulder, elbow, wrist)
                        angles_data['elbow'].append(elbow_angle)
                        
                        # Hip-Shoulder-Elbow angle (Shoulder angle)
                        hip = self.get_landmark_coords(landmarks, self.mp_pose.PoseLandmark.RIGHT_HIP.value)
                        shoulder_angle = self.calculate_angle(hip, shoulder, elbow)
                        angles_data['shoulder'].append(shoulder_angle)
                        
                        # Hip-Knee-Ankle angle (Knee bend)
                        knee = self.get_landmark_coords(landmarks, self.mp_pose.PoseLandmark.RIGHT_KNEE.value)
                        ankle = self.get_landmark_coords(landmarks, self.mp_pose.PoseLandmark.RIGHT_ANKLE.value)
                        knee_angle = self.calculate_angle(hip, knee, ankle)
                        angles_data['knee'].append(knee_angle)
                        
                        # Shoulder-Hip-Knee angle (Hip angle)
                        hip_angle = self.calculate_angle(shoulder, hip, knee)
                        angles_data['hip'].append(hip_angle)
                        
                    except Exception as e:
                        print(f"Error processing frame {frame_count}: {e}")
                        continue
        
        finally:
            cap.release()
        
        if processed_frames == 0:
            raise ValueError("No valid pose detected in video. Please ensure the shooter is clearly visible.")
        
        # Calculate analysis results
        analysis_result = {
            'elbow_angle': self._safe_mean(angles_data['elbow']),
            'shoulder_angle': self._safe_mean(angles_data['shoulder']),
            'knee_angle': self._safe_mean(angles_data['knee']),
            'hip_angle': self._safe_mean(angles_data['hip']),
            'release_angle': self.estimate_release_angle(angles_data),
            'body_alignment_score': self.calculate_alignment_score(angles_data),
            'frames_processed': processed_frames,
            'total_frames': frame_count
        }
        
        return analysis_result
    
    def _safe_mean(self, data_list):
        """Calculate mean safely, handling empty lists"""
        if data_list and len(data_list) > 0:
            return round(float(np.mean(data_list)), 2)
        return 0.0
    
    def estimate_release_angle(self, angles_data):
        """Estimate optimal release angle from elbow extension"""
        if angles_data['elbow'] and len(angles_data['elbow']) > 0:
            # Release typically occurs at maximum elbow extension
            max_elbow = max(angles_data['elbow'])
            # Optimal release angle is typically 48-52 degrees
            estimated_angle = min(max_elbow * 0.45, 55)
            return round(estimated_angle, 2)
        return 50.0
    
    def calculate_alignment_score(self, angles_data):
        """
        Calculate overall body alignment score (0-100)
        Based on comparison with ideal shooting form
        """
        # Ideal angles for perfect shooting form
        ideal_angles = {
            'elbow': 95,      # 90-100 degrees
            'shoulder': 135,  # 130-140 degrees
            'knee': 160,      # 155-165 degrees
            'hip': 175        # 170-180 degrees
        }
        
        scores = []
        
        for angle_type, ideal_value in ideal_angles.items():
            if angles_data[angle_type] and len(angles_data[angle_type]) > 0:
                actual_avg = np.mean(angles_data[angle_type])
                # Calculate deviation from ideal
                deviation = abs(actual_avg - ideal_value)
                # Score decreases with deviation (max 100, min 0)
                score = max(0, 100 - (deviation * 2))
                scores.append(score)
        
        overall_score = np.mean(scores) if scores else 0
        return round(float(overall_score), 2)
    
    def generate_feedback(self, analysis_result):
        """
        Generate intelligent AI feedback based on analysis results
        Returns list of feedback dictionaries
        """
        feedbacks = []
        
        elbow = analysis_result.get('elbow_angle', 0)
        shoulder = analysis_result.get('shoulder_angle', 0)
        knee = analysis_result.get('knee_angle', 0)
        hip = analysis_result.get('hip_angle', 0)
        alignment = analysis_result.get('body_alignment_score', 0)
        
        # Elbow feedback
        if elbow < 85:
            feedbacks.append({
                'type': 'Elbow Position',
                'text': f'Your elbow angle ({elbow:.1f}°) is too acute.',
                'suggestion': 'Extend your elbow more during the release. Aim for 90-100 degrees for optimal shot mechanics.',
                'priority': 3
            })
        elif elbow > 105:
            feedbacks.append({
                'type': 'Elbow Position',
                'text': f'Your elbow angle ({elbow:.1f}°) is too extended.',
                'suggestion': 'Bend your elbow slightly more for better control and power. Target 90-100 degrees.',
                'priority': 2
            })
        else:
            feedbacks.append({
                'type': 'Elbow Position',
                'text': f'Excellent elbow angle ({elbow:.1f}°)!',
                'suggestion': 'Maintain this elbow position for consistent shooting form.',
                'priority': 1
            })
        
        # Shoulder feedback
        if shoulder < 125:
            feedbacks.append({
                'type': 'Shoulder Alignment',
                'text': f'Your shoulder angle ({shoulder:.1f}°) is too low.',
                'suggestion': 'Raise your shooting arm higher. Keep shoulder angle around 130-140 degrees for better arc.',
                'priority': 3
            })
        elif shoulder > 145:
            feedbacks.append({
                'type': 'Shoulder Alignment',
                'text': f'Your shoulder angle ({shoulder:.1f}°) is too high.',
                'suggestion': 'Lower your shooting elbow slightly. Aim for 130-140 degrees.',
                'priority': 2
            })
        
        # Knee feedback
        if knee < 150:
            feedbacks.append({
                'type': 'Leg Position',
                'text': f'Your knees are too bent ({knee:.1f}°).',
                'suggestion': 'Straighten your legs more during the shot. Use leg power efficiently with 155-165 degree angle.',
                'priority': 2
            })
        elif knee > 170:
            feedbacks.append({
                'type': 'Leg Position',
                'text': 'Your legs are too straight.',
                'suggestion': 'Bend your knees slightly more to generate power from your legs.',
                'priority': 2
            })
        
        # Overall alignment feedback
        if alignment >= 85:
            feedbacks.append({
                'type': 'Overall Form',
                'text': f'Outstanding shooting form! (Score: {alignment:.1f}/100)',
                'suggestion': 'Your technique is excellent. Focus on maintaining this consistency in every shot.',
                'priority': 1
            })
        elif alignment >= 70:
            feedbacks.append({
                'type': 'Overall Form',
                'text': f'Good shooting form with room for improvement. (Score: {alignment:.1f}/100)',
                'suggestion': 'Focus on the specific corrections mentioned above to improve your score.',
                'priority': 2
            })
        else:
            feedbacks.append({
                'type': 'Overall Form',
                'text': f'Your shooting form needs significant improvement. (Score: {alignment:.1f}/100)',
                'suggestion': 'Work on fundamental shooting mechanics. Consider working with a coach and reviewing basic form.',
                'priority': 3
            })
        
        return feedbacks
    
    def __del__(self):
        """Cleanup resources"""
        if hasattr(self, 'pose'):
            self.pose.close()
