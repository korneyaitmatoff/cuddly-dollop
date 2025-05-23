from lib2to3.pgen2.tokenize import group

from app import create_app
from app.models import db
from app.models.employee import Employee
from app.models.student import Student
from app.models.medical_card import MedicalRecord  # Assuming this model exists
from datetime import datetime

app = create_app('development')

with app.app_context():
    # Create all tables
    db.create_all()

    # Check if there are already employees
    if Employee.query.count() == 0:
        # Create admin user
        admin = Employee(
            username='admin',
            email='admin@example.com',
            first_name='Admin',
            last_name='User',
            position='Administrator',
            department='IT',
            hire_date=datetime.now(),
            salary=100000.00,
            is_admin=True
        )
        admin.password = 'password123'

        db.session.add_all([admin])
        db.session.commit()

        print("Database initialized with sample employees.")
    else:
        print("Database already contains employees.")

    # Add student and his medical records
    if Student.query.count() == 0:
        # Create sample students
        student1 = Student(
            first_name='John',
            last_name='Doe',
            date_of_birth=datetime(2000, 1, 15),
            group="IO-123"
        )

        student2 = Student(
            first_name='Jane',
            last_name='Smith',
            date_of_birth=datetime(2001, 5, 20),
            group="IO-234"
        )

        # Add students to session
        db.session.add_all([student1, student2])
        db.session.commit()

        # Create medical records for students
        med_record1 = MedicalRecord(
            student_id=student1.id,
            date=datetime.now(),
            record_type="note",
            description='Seasonal allergies',
            doctor='Dr. Johnson'
        )

        med_record2 = MedicalRecord(
            student_id=student1.id,
            date=datetime.now(),
            record_type="note",
            description='Seasonal allergies',
            doctor='Dr. Johnson'
        )

        med_record3 = MedicalRecord(
            student_id=student2.id,
            record_date=datetime.now(),
            condition='None',
            treatment='None',
            notes='Annual checkup, all clear',
            doctor_name='Dr. Brown'
        )

        # Add medical records to session
        db.session.add_all([med_record1, med_record2, med_record3])
        db.session.commit()

        print("Database initialized with sample students and medical records.")
    else:
        print("Database already contains students.")
