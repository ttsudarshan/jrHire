from app import db
from datetime import datetime, timezone

class Job(db.Model):
    __tablename__ = 'jobs'

    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(100), nullable=False)
    job_title = db.Column(db.String(100), nullable=False)
    job_type = db.Column(db.String(100), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    introduction = db.Column(db.Text, nullable=True)
    time_period = db.Column(db.String(50), nullable=True)
    compensation_per_hour = db.Column(db.Integer, nullable=True)
    description = db.Column(db.Text, nullable=True)
    benefits = db.Column(db.Text, nullable=True)
    requirements = db.Column(db.Text, nullable=True)
    location = db.Column(db.String(100), nullable=True)
    tags = db.Column(db.String(200), nullable=True)
    profile_colors = db.Column(db.String(100), nullable=True)
    url_ats = db.Column(db.Text, nullable=True)  
    
    is_remote = db.Column(db.Boolean, nullable=True)
    is_paid = db.Column(db.Boolean, nullable=True)
    is_worldwide = db.Column(db.Boolean, nullable=True)

    def __init__(self, company_name, job_title, job_type=None, introduction=None, time_period=None, compensation_per_hour=None,
                 description=None, benefits=None, requirements=None, location=None, tags=None, profile_colors=None, url_ats=None,
                 is_remote=None, is_paid=None, is_worldwide=None):
        self.company_name = company_name
        self.job_title = job_title
        self.job_type = job_type
        self.introduction = introduction
        self.time_period = time_period
        self.compensation_per_hour = compensation_per_hour
        self.description = description
        self.benefits = benefits
        self.requirements = requirements
        self.location = location
        self.tags = tags
        self.profile_colors = profile_colors
        self.is_remote = is_remote
        self.is_paid = is_paid
        self.is_worldwide = is_worldwide
        self.url_ats = url_ats
    def __repr__(self):
        return f"<Job {self.company_name} - {self.job_title}>"

    