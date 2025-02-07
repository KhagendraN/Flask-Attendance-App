# Attendance Management System

The Attendance Management System is a web application designed to streamline the process of managing attendance for educational institutions. This system allows users to register, log in, and efficiently manage attendance records.

## Features

### User Registration & Login
- Users can create an account with email and password authentication.
- After logging in, users are directed to the setup page.

### Setup Page
- Add Subjects: Users can add subjects.
- Add Teachers: Assign teachers to specific subjects.
- Add Students: Enter student details (Name & Roll Number).

### Home Page
- Display a dashboard with the following options:
  - Select Subject (Dropdown or List)
  - Select Teacher (Dropdown or List)
  - Take Attendance

### Attendance Page
- Display a list of students with their names and roll numbers.
- Each student has an option to be marked Present or Absent.
- Once attendance is marked, a Confirm Attendance button finalizes the entry.

### Attendance Records & Reports
- Option to Download Attendance Records by selecting a Start Date and End Date.
- Users can view and export records in Excel/PDF format.
- Feature to Delete Records from a selected date range.

## Additional Requirements

- The web app should be responsive and mobile-friendly.
- Data should be stored securely (consider Firebase, MySQL, or MongoDB).
- Include role-based access (e.g., Admin, Teachers).
- Use a clean UI with intuitive navigation and proper validation.

## Getting Started

### Prerequisites
- Ensure you have Python and Flask installed.
- Set up a virtual environment:
  ```sh
  python -m venv venv
  source venv/bin/activate
  ```

### Installation
1. Clone the repository:
   ```sh
   git clone https://github.com/yourusername/attendance-management-system.git
   cd attendance-management-system
   ```

2. Install the required dependencies:
   ```sh
   pip install -r requirements.txt
   ```

3. Set up the database:
   - Ensure you have SQLite installed.
   - Run the migrations to set up the database schema:
     ```sh
     flask db upgrade
     ```

4. Run the application:
   ```sh
   flask run
   ```

5. Access the application:
   - Open your web browser and navigate to `http://127.0.0.1:5000` to use the attendance management system.

## Contributing

Contributions are welcome! Please follow these steps:
1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch-name`).
3. Commit your changes (`git commit -am 'Add some feature'`).
4. Push to the branch (`git push origin feature-branch-name`).
5. Create a new Pull Request.

## License

This project is licensed under the MIT License.
