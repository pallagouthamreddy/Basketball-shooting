# Basketball AI Analysis System 🏀

AI-powered basketball shooting analysis platform built with Django, MySQL, OpenCV and MediaPipe. Players upload shooting videos, the system detects body pose, measures shooting-form angles, and returns feedback and progress tracking.

Based on the review paper *A Review of Basketball Shooting Analysis Based on Artificial Intelligence*.

## Demo

https://youtu.be/AXd3cePz_Go

## Features

- **User management**: registration, login, player and coach roles, profiles
- **Video upload**: upload shooting videos from training, practice or matches
- **AI pose detection**: MediaPipe pose estimation on each video
- **Posture analysis**: elbow, shoulder, knee, hip and release angles plus a body-alignment score
- **Trajectory analysis**: arc height, release velocity, predicted success rate
- **AI feedback**: prioritised corrections and suggestions per session
- **Performance analytics**: progress tracking across sessions
- **Admin dashboard**: system-wide monitoring and management

## How It Works

```
User uploads a shooting video
        |
shooting/views.py receives it and creates a ShootingSession
        |
shooting/pose_analyzer.py (PoseAnalyzer)
  - OpenCV reads the video frame by frame
  - MediaPipe detects body landmarks
  - Joint angles and form measurements are calculated
        |
Results saved to MySQL:
  PostureAnalysis, TrajectoryAnalysis, AIFeedback
        |
Dashboard pages show results, feedback and progress
```

## Tech Stack

Python, Django 5.2, MySQL, OpenCV, MediaPipe, NumPy, Pillow, Bootstrap 5 (django-crispy-forms), python-decouple

## Project Structure

```
├── manage.py
├── config/                  # Django settings and root URLs
├── accounts/                # Custom user model, auth, profiles
├── shooting/                # Video upload, pose_analyzer.py, analysis models
├── analytics/               # Performance tracking
├── ml_models/               # ML model management
├── dashboard/               # User and admin dashboards
├── templates/               # HTML templates
├── static/                  # Static assets
├── generate_sample_data.py  # Creates demo users and sessions
├── requirements.txt
└── .env.example
```

Uploaded videos go to `media/` and are not stored in the repository.

## Requirements

- **Python 3.11 or 3.12**. Do not use 3.13: MediaPipe versions that include the `mp.solutions` API have no build for it.
- **MediaPipe 0.10.14 or older** (newer releases removed `mp.solutions`)
- **MySQL 8.0 or later** with Django 5.x (Django 6.x needs MySQL 8.4+)
- Git

Exact package versions are in `requirements.txt`.

## Setup

```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPO.git
cd YOUR_REPO

python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # Linux / macOS

pip install -r requirements.txt
```

**1. Configure environment.** Copy `.env.example` to `.env` and fill in your own secret key and MySQL password.

**2. Create the database.**

```sql
CREATE DATABASE basketball_analysis_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

**3. Migrate and run.**

```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Open http://127.0.0.1:8000/shooting/

## Sample Data

Fills the database with demo players, coach, sessions and feedback:

```bash
python generate_sample_data.py
```

| Username | Password |
|---|---|
| player1 to player5 | password123 |
| coach1 | password123 |

These are demo accounts for local testing only.

## Future Work

- Combine computer vision with biomechanics to judge the rationality of shooting actions
- Real-time analysis for training and game scenarios
- Personalised shooting analysis and training plans
