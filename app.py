from flask import Flask, render_template, request, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired, Email
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import requests
from datetime import datetime
import pytz
import smtplib
import os

app = Flask(__name__)
# database_url= os.environ.get("postgresql://postgres:Mango123@localhost/postgres")
database_url = os.environ.get("DATABASE_URL")
# Set a default local database URL for development
if database_url is None:
    database_url = "postgresql://postgres:Mango123@localhost:5432/postgres"
app.config['SECRET_KEY'] = 'muhee'
app.config["SQLALCHEMY_DATABASE_URI"] = database_url
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Mango123@localhost/postgres'
db = SQLAlchemy(app)

class Task1(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    shift = db.Column(db.String(50), nullable=False)
    time = db.Column(db.DateTime, default=datetime.now(pytz.timezone('Asia/Kolkata')), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    reports = db.Column(db.String(200))

with app.app_context():
    db.create_all()

class Task1Form(FlaskForm):
    shift = StringField('Shift', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    reports = TextAreaField('Reports')

# Function to send email
def send_email(task, message=""):
    from_email = 'blasterb954@gmail.com'
    to_email = 'muheem1002@gmail.com'
    
    subject = 'Task Done'
    message = f"Task done by {task.name} for shift {task.shift}, reports done are {task.reports}."

    try:
        msg = MIMEMultipart()
        msg['From'] = from_email
        msg['To'] = to_email
        msg['Subject'] = subject
        msg.attach(MIMEText(message, 'plain'))

        smtp_server = 'smtp.gmail.com'
        smtp_port = 587
        smtp_username = 'blasterb954@gmail.com'
        smtp_password = 'nsbq azad hqte qquv'

        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_username, smtp_password)

        server.sendmail(from_email, to_email, msg.as_string())
        server.quit()

        print(f"Email sent to {to_email}")
    except Exception as e:
        print(f"Email not sent. Error: {str(e)}")

def send_slack(task):
    slack_url = 'https://hooks.slack.com/services/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'
    message = f"Task done by {task.name} for shift {task.shift}, reports done are {task.reports}."

    payload = {
        'text': message
    }

    response = requests.post(slack_url, json=payload)
# Function to get task by name and email
def get_task_by_name_and_email(name, email):
    return Task1.query.filter_by(name=name, email=email).first()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/task_management', methods=['GET', 'POST'])
def task_management():
    form = Task1Form()
    print("shift: ",form.shift.data)
    print("name: ",form.name.data)
    print("email: ",form.email.data)
    print("reportsTo: ",form.reports.data)
    if request.method == 'POST' and form.validate_on_submit():
        task = Task1(
            shift=form.shift.data,
            name=form.name.data,
            email=form.email.data,
            reports=form.reports.data,
        )
        db.session.add(task)
        db.session.commit()
        send_email(task)
        send_slack(task)
        flash('Task done and notifications sent.', 'success')
        return redirect(url_for('task_management'))

    tasks1 = Task1.query.all()
    return render_template('task_management.html', form=form, tasks1=tasks1)

@app.route('/task_management', methods=['PUT', 'DELETE'])
def update_or_delete_task():
    name = request.form.get('name')
    email = request.form.get('email')

    task = get_task_by_name_and_email(name, email)

    if not task:
        flash('Task not found.', 'error')
        return redirect(url_for('task_management'))

    if request.method == 'PUT':
        task.shift = request.form.get('shift')
        task.reports = request.form.get('reports')
        db.session.commit()
        flash('Task updated successfully.', 'success')
        return redirect(url_for('task_management'))

    if request.method == 'DELETE':
        db.session.delete(task)
        db.session.commit()
        flash('Task deleted successfully.', 'success')
        return redirect(url_for('task_management'))

if __name__ == '__main__':
    app.run(debug=True)
