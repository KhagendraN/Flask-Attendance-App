from flask import Flask, render_template, request, redirect, url_for, send_file, flash
from models import db, Attendance, Student
from datetime import datetime
import pandas as pd
from fpdf import FPDF
from flask_sqlalchemy import SQLAlchemy
import io, secrets, os
from flask_migrate import Migrate

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')   
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

migrate = Migrate(app, db)

@app.route('/')
def home():
    subjects = ['Mathematics', 'Physics', 'FEEE','C Programming', 'Drawing','workshop']  # Example subjects
    teachers = ['BRT', 'UKJ',"PA","HPG","GBT","JKM"]   # Example teachers
    return render_template('home.html', subjects=subjects, teachers=teachers)

@app.route('/take_attendance', methods=['POST'])
def take_attendance():
    subject = request.form['subject']
    teacher = request.form['teacher']
    date = datetime.now().date()
    
    # Check if today's attendance column exists for the subject and teacher, if not create it
    existing_column = f"date_{date}"
    
    # Retrieve students and their details
    students = Student.query.all()
    for student in students:
        attendance = Attendance(subject=subject, teacher=teacher, date=date, 
                                 roll_number=student.roll_number, student_name=student.name, status='A')
        db.session.add(attendance)
    db.session.commit()
    
    return redirect(url_for('attendance', subject=subject, teacher=teacher, date=date))

@app.route('/attendance', methods=['GET', 'POST'])
def attendance():
    subject = request.args.get('subject')
    teacher = request.args.get('teacher')
    date = request.args.get('date')
    
    students = Student.query.all()  # Fetch all students from the database
    
    if request.method == 'POST':
        # Collect attendance status for each student
        for student in students:
            # Get the attendance status from the form (using roll number as the key)
            status = request.form.get(f"attendance_{student.roll_number}")
            # Find the attendance entry for this student and update their status
            attendance = Attendance.query.filter_by(subject=subject, teacher=teacher, 
                                                    date=date, roll_number=student.roll_number).first()
            if attendance:
                attendance.status = status  # Update status
        db.session.commit()  # Commit changes to the database
        return redirect(url_for('confirm'))  # Redirect to confirmation page

    return render_template('attendance.html', students=students, subject=subject, 
                           teacher=teacher, date=date)





# Set a secret key for session management
app.secret_key = secrets.token_hex(16)  # Change this to a unique key

@app.route('/confirm', methods=['GET', 'POST'])
def confirm():
    if request.method == 'POST':
        # Hardcoded password (you can change it to anything you like)
        correct_password = "admin123"
        
        entered_password = request.form.get('password')
        
        if entered_password == correct_password:
            # If the password is correct, proceed with confirmation
            flash('Attendance Confirmed Successfully!', 'success')
            return redirect(url_for('confirm'))  # Redirect to the same page or another page
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

    # Get attendance data filtered by subject, teacher, and date range
    attendances = Attendance.query.filter(
        Attendance.subject == subject, 
        Attendance.teacher == teacher, 
        Attendance.date >= start_date, 
        Attendance.date <= end_date
    ).all()

    # Convert to a better structured dictionary
    attendance_data = {}
    for att in attendances:
        if att.roll_number not in attendance_data:
            attendance_data[att.roll_number] = {
                "Roll Number": att.roll_number,
                "Student Name": att.student_name
            }
        attendance_data[att.roll_number][str(att.date)] = att.status

    # Convert to DataFrame for Excel output
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

        col_width = 40  # Adjust column width

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