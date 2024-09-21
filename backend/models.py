from app import db
from datetime import datetime

class JobApplication(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(100), nullable=False)
    position = db.Column(db.String(100), nullable=False)
    application_date = db.Column(db.Date, nullable=False)
    interview_date = db.Column(db.Date)
    status = db.Column(db.String(20), nullable=False, default='Pending')
    follow_up_date = db.Column(db.Date)
    notes = db.Column(db.Text)

    def __repr__(self):
        return f'<JobApplication {self.company_name}, {self.position}>'
