from flask import Flask, render_template, request, redirect, url_for, send_file, flash
from models import db, Attendance, Student  # Import models
from datetime import datetime
import pandas as pd
from fpdf import FPDF
from flask_sqlalchemy import SQLAlchemy
import io, secrets, os
from flask_migrate import Migrate

app = Flask(__name__)

# Database Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///attendance.db')  # Fallback to SQLite if env variable is missing
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize Database
db.init_app(app)
migrate = Migrate(app, db)

# Ensure models are created
with app.app_context():
    db.create_all()

# Secret Key for session management
app.secret_key = secrets.token_hex(16)

@app.route('/')
def home():
    subjects = ['Mathematics', 'Physics', 'FEEE', 'C Programming', 'Drawing', 'Workshop']
    teachers = ['BRT', 'UKJ', "PA", "HPG", "GBT", "JKM"]
    return render_template('home.html', subjects=subjects, teachers=teachers)

@app.route('/take_attendance', methods=['POST'])
def take_attendance():
    subject = request.form['subject']
    teacher = request.form['teacher']
    date = datetime.now().date()

    students = Student.query.all()

    for student in students:
        existing_attendance = Attendance.query.filter_by(
            subject=subject, teacher=teacher, date=date, roll_number=student.roll_number
        ).first()

        if not existing_attendance:
            attendance = Attendance(
                subject=subject, teacher=teacher, date=date,
                roll_number=student.roll_number, student_name=student.name, status='A'
            )
            db.session.add(attendance)

    db.session.commit()
    
    return redirect(url_for('attendance', subject=subject, teacher=teacher, date=date))

@app.route('/attendance', methods=['GET', 'POST'])
def attendance():
    subject = request.args.get('subject')
    teacher = request.args.get('teacher')
    date = request.args.get('date')

    students = Student.query.all()

    if request.method == 'POST':
        for student in students:
            status = request.form.get(f"attendance_{student.roll_number}")
            attendance = Attendance.query.filter_by(
                subject=subject, teacher=teacher, date=date, roll_number=student.roll_number
            ).first()
            if attendance:
                attendance.status = status  
        db.session.commit()
        return redirect(url_for('confirm')) 

    return render_template('attendance.html', students=students, subject=subject, teacher=teacher, date=date)

@app.route('/confirm', methods=['GET', 'POST'])
def confirm():
    if request.method == 'POST':
        correct_password = "admin123"
        entered_password = request.form.get('password')
        
        if entered_password == correct_password:
            flash('Attendance Confirmed Successfully!', 'success')
            return redirect(url_for('confirm'))  
        else:
            flash('Incorrect password. Please try again.', 'danger')
    
    return render_template('confirm.html')

@app.route('/download')
def download():
    return render_template('download.html')

@app.route('/generate_report', methods=['POST'])
def generate_report():
    subject = request.form['subject']
    teacher = request.form['teacher']
    start_date = request.form['start_date']
    end_date = request.form['end_date']

    attendances = Attendance.query.filter(
        Attendance.subject == subject, 
        Attendance.teacher == teacher, 
        Attendance.date >= start_date, 
        Attendance.date <= end_date
    ).all()

    attendance_data = {}
    for att in attendances:
        if att.roll_number not in attendance_data:
            attendance_data[att.roll_number] = {
                "Roll Number": att.roll_number,
                "Student Name": att.student_name
            }
        attendance_data[att.roll_number][str(att.date)] = att.status

    df = pd.DataFrame(list(attendance_data.values()))

    output = io.BytesIO()

    if request.form['format'] == 'excel':
        df.to_excel(output, index=False)
        output.seek(0)
        return send_file(output, as_attachment=True, download_name="attendance.xlsx", mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

    elif request.form['format'] == 'pdf':
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        pdf.cell(200, 10, txt=f"Attendance Report: {subject} ({teacher})", ln=True, align="C")

        col_width = 40  

        headers = list(df.columns)
        for header in headers:
            pdf.cell(col_width, 10, header, border=1)

        pdf.ln()

        for _, row in df.iterrows():
            for value in row:
                pdf.cell(col_width, 10, str(value), border=1)
            pdf.ln()

        output = io.BytesIO()
        pdf.output(output)
        output.seek(0)
        return send_file(output, as_attachment=True, download_name="attendance.pdf", mimetype="application/pdf")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
