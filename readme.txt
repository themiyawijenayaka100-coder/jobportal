JOB PORTAL (Django Web Application)
==================================

Job Portal is a Django-based web application that connects job seekers with employers.
It supports job posting, job applications, user profiles, stories, and notifications.


TECH STACK
----------
- Backend: Django (Python)
- Database: SQLite (default, db.sqlite3)
- UI: Bootstrap 5
- Forms: django-crispy-forms + crispy-bootstrap5
- Media: Pillow (for profile pictures)


PROJECT APPS / MODULES
---------------------
- accounts
  - Authentication (register/login/logout)
  - User profiles (bio, skills, experience, education, profile picture, CV file, resume link)
  - Talent list (Hire Talent)
  - Direct messages (inbox + send message)
  - Notifications

- jobs
  - Jobs (create/list/apply)
  - Stories (create/list)

- applications
  - Job applications tracking (My Applications)


FEATURES
--------
- User registration and login
- Role-based behavior (Employer vs Candidate)
- Create and browse job listings
- Apply to jobs and track application status (Pending/Accepted/Rejected)
- Employer job posting
- Profile management (edit profile + upload profile picture/CV)
- Hire Talent (browse candidate profiles)
- Stories (share experiences)
- Notifications and messaging inbox


QUICK START (LOCAL SETUP)
------------------------
1) Create & activate a virtual environment

   Windows (PowerShell):
     python -m venv .venv
     .\.venv\Scripts\Activate.ps1

2) Install dependencies

     pip install -r requirements.txt

3) Run migrations

     python manage.py migrate

4) (Optional) Create an admin user

     python manage.py createsuperuser

5) Run the development server

     python manage.py runserver

Then open:
  http://127.0.0.1:8000/


DEFAULT ROUTES (IMPORTANT PAGES)
-------------------------------
- Home: /
- About: /about/
- Find Jobs: /jobs/
- Create Job: /jobs/create/
- My Applications: /applications/my/
- Hire Talent: /talents/
- Edit Profile: /profile/edit/
- Profile Detail: /profile/<user_id>/
- Notifications: /notifications/
- Admin: /admin/


FILES & UPLOADS (MEDIA)
-----------------------
This project uses file uploads for:
- Profile pictures
- CV files

In development, make sure MEDIA settings and URL serving are configured if you want to view uploaded files.


DEPENDENCIES
------------
See: requirements.txt
- Django>=6.0
- Pillow>=12.2
- django-crispy-forms>=2.4
- crispy-bootstrap5>=2025.6


NOTES
-----
- This repository currently uses SQLite for simplicity.
- For production, configure:
  - DEBUG=False
  - ALLOWED_HOSTS
  - SECRET_KEY via environment variables
  - A production-ready database (PostgreSQL/MySQL)
  - Static/media hosting

