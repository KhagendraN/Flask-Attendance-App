from app import app, db
from models import Student

# Create app context
with app.app_context():
    for i in range(1, 49):
        std = input(f"Enter student name {i}: ")  # Get the actual name
        
        student = db.session.query(Student).filter_by(roll_number=i).first()  # Find existing student
        if student:
            student.name = std  # Update the name
        else:
            print(f"Student with roll number {i} not found. Skipping...")

    db.session.commit()
    print("Student names have been updated successfully.")

# from app import app, db
# from models import Student

# with app.app_context():
#     roll_number = int(input("Enter the roll number to update: "))
#     new_name = input("Enter the new name: ")

#     student = db.session.query(Student).filter_by(roll_number=roll_number).first()

#     if student:
#         student.name = new_name
#         db.session.commit()
#         print(f"Updated roll number {roll_number} to '{new_name}'.")
#     else:
#         print(f"Student with roll number {roll_number} not found.")

# from app import app, db
# from models import Student

# # Create app context
# with app.app_context():
#     # Delete all existing students
#     Student.query.delete()

#     # Adding dummy students
#     for i in range(1, 49):
#         student = Student(roll_number=i, name=f"Student {i}")
#         db.session.add(student)

#     db.session.commit()

#     print("Dummy students have been added to the database.")
