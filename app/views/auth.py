from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from app.models.employee import Employee
from app.models import db

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        employee = Employee.query.filter_by(username=username).first()

        if employee is not None and employee.verify_password(password):
            login_user(employee)
            next_page = request.args.get('next')
            if next_page is None or not next_page.startswith('/'):
                next_page = url_for('main.index')
            flash('Вы успешно авторизованы!', 'success')
            return redirect(next_page)
        else:
            flash('Неверный логин или пароль', 'error')

    return render_template('auth/login.html')


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out', 'success')
    return redirect(url_for('main.index'))


# This route is for development purposes to create initial users
@auth.route('/setup')
def setup():
    if Employee.query.count() > 0:
        flash('Setup has already been completed', 'error')
        return redirect(url_for('main.index'))

    # Create admin user
    admin = Employee(
        username='admin',
        email='admin@example.com',
        first_name='Admin',
        last_name='User',
        position='Administrator',
        department='IT',
        is_admin=True
    )
    admin.password = 'password123'

    # Create regular employee
    employee = Employee(
        username='employee',
        email='employee@example.com',
        first_name='John',
        last_name='Doe',
        position='Developer',
        department='Engineering',
        salary=75000.00
    )
    employee.password = 'employee123'

    db.session.add_all([admin, employee])
    db.session.commit()

    flash('Initial users created successfully', 'success')
    return redirect(url_for('auth.login'))
