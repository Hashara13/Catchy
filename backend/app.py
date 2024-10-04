
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
from flask_cors import CORS
import matplotlib.pyplot as plt
import os

app = Flask(__name__)
CORS(app) 
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///jobs.db'
# app.config['MAIL_SERVER'] = 'smtp.example.com'
# app.config['MAIL_PORT'] = 587
# app.config['MAIL_USERNAME'] = 'your_email@example.com'
# app.config['MAIL_PASSWORD'] = 'your_password'
# app.config['MAIL_USE_TLS'] = True
mail = Mail(app)
db = SQLAlchemy(app)

class JobApplication(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(100), nullable=False)
    position = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(20), nullable=False, default='Pending')
    application_date = db.Column(db.String(20), nullable=False)
    interview_date = db.Column(db.String(20))
    follow_up_date = db.Column(db.String(20))
    notes = db.Column(db.Text)

with app.app_context():
    db.create_all()

@app.route('/add_application', methods=['POST'])
def add_application():
    data = request.json
    new_application = JobApplication(
        company_name=data['company_name'],
        position=data['position'],
        status=data['status'],
        application_date=data['application_date'],
        interview_date=data.get('interview_date', ''),
        follow_up_date=data.get('follow_up_date', ''),
        notes=data.get('notes', '')
    )
    db.session.add(new_application)
    db.session.commit()
    return jsonify({'message': 'Application added successfully!'})

@app.route('/applications', methods=['GET'])
def get_applications():
    applications = JobApplication.query.all()
    app_list = [{'company_name': app.company_name, 'position': app.position, 'status': app.status,
                 'application_date': app.application_date, 'interview_date': app.interview_date,
                 'follow_up_date': app.follow_up_date, 'notes': app.notes} for app in applications]
    return jsonify(app_list)

@app.route('/progress_chart', methods=['GET'])
def generate_chart():
    statuses = {'Pending': 0, 'Interview Scheduled': 0, 'Accepted': 0, 'Rejected': 0}
    applications = JobApplication.query.all()
    for app in applications:
        statuses[app.status] += 1

    labels = statuses.keys()
    sizes = statuses.values()

    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
    plt.axis('equal')

    if not os.path.exists('static'):
        os.mkdir('static')

    chart_path = 'static/progress_chart.png'
    plt.savefig(chart_path)
    return jsonify({'chart_url': f'/static/progress_chart.png'})

@app.route('/send_reminder', methods=['POST'])
def send_reminder():
    data = request.json
    recipient = data['email']
    subject = 'Follow-Up Reminder'
    body = data['message']

    msg = Message(subject, recipients=[recipient], body=body)
    mail.send(msg)
    return jsonify({'message': 'Reminder sent successfully!'})

if __name__ == '__main__':
    app.run(debug=True)
