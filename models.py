from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()

class Attendance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(100))
    teacher = db.Column(db.String(100))
    date = db.Column(db.Date)
    roll_number = db.Column(db.Integer)
    student_name = db.Column(db.String(100))
    status = db.Column(db.String(1))  # 'P' for present, 'A' for absent

    def __init__(self, subject, teacher, date, roll_number, student_name, status):
        self.subject = subject
        self.teacher = teacher
        self.date = date
        self.roll_number = roll_number
        self.student_name = student_name
        self.status = status

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    roll_number = db.Column(db.Integer, unique=True)
    name = db.Column(db.String(100))

    def __init__(self, roll_number, name):
        self.roll_number = roll_number
        self.name = name
