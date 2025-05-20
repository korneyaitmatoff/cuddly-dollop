from app import create_app
from app.models import db
from app.models.employee import Employee
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
