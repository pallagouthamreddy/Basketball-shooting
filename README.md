# Basketball AI Analysis System 🏀

AI-powered basketball shooting analysis platform using Django, MySQL, and MediaPipe.

## Features

✅ **User Management** - Registration, authentication, and profiles  
✅ **Video Upload** - Upload shooting videos for analysis  
✅ **AI Pose Detection** - MediaPipe-powered pose estimation  
✅ **Performance Analytics** - Track progress over time  
✅ **AI Feedback** - Intelligent corrections and suggestions  
✅ **Admin Dashboard** - System-wide monitoring and management  

## Quick Start

### 1. Prerequisites
- Python 3.11.9
- MySQL Server
- Git

### 2. Installation

```bash
# Clone or create project directory
mkdir basketball_analysis_system
cd basketball_analysis_system

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start Server
python manage.py runserver

Sample Users:

Username: player1 | Password: password123

Username: player2 | Password: password123
```
# Project Structure

basketball_analysis_system/
├── accounts/          # User management
├── shooting/          # Video upload & AI analysis
├── analytics/         # Performance tracking
├── ml_models/         # ML model management
├── dashboard/         # User & admin dashboards
├── templates/         # HTML templates
├── media/            # Uploaded files
└── static/           # Static assets
