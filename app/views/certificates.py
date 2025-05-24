from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from app.models import db
from app.models.student import Student
from datetime import datetime
import random
import string

certificates = Blueprint('certificates', __name__, url_prefix='/certificates')

# Helper function to generate certificate number
def generate_certificate_number():
    prefix = "MED"
    random_part = ''.join(random.choices(string.digits, k=8))
    return f"{prefix}-{random_part}"

# Dictionary mapping certificate types to their full names
CERTIFICATE_TYPES = {
    'general': 'Общая медицинская справка',
    'sports': 'Справка для занятий спортом',
    'absence': 'Справка о болезни',
    'vaccination': 'Справка о вакцинации'
}

# Dictionary with default conclusions for each certificate type
DEFAULT_CONCLUSIONS = {
    'general': 'Здоров(а). Противопоказаний не выявлено.',
    'sports': 'Допущен(а) к занятиям физической культурой и спортом.',
    'absence': 'Перенес(ла) заболевание. К учебным занятиям допущен(а).',
    'vaccination': 'Вакцинация проведена в соответствии с календарем прививок.'
}

# Dictionary with default recommendations for each certificate type
DEFAULT_RECOMMENDATIONS = {
    'general': 'Особых рекомендаций нет.',
    'sports': 'Рекомендуется умеренная физическая нагрузка.',
    'absence': 'Рекомендуется щадящий режим в течение 7 дней.',
    'vaccination': 'Наблюдение в течение 3 дней после вакцинации.'
}

@certificates.route('/generate', methods=['GET', 'POST'])
@login_required
def generate():
    if request.method == 'POST':
        student_id = request.form.get('student_id')
        certificate_type = request.form.get('certificate_type')
        issue_date = request.form.get('issue_date')
        doctor = request.form.get('doctor')

        if not all([student_id, certificate_type, issue_date, doctor]):
            flash('Пожалуйста, заполните все поля формы', 'error')
            return redirect(url_for('certificates.generate'))

        # Redirect to the certificate view page with parameters
        return redirect(url_for('certificates.view_certificate',
                               student_id=student_id,
                               certificate_type=certificate_type,
                               issue_date=issue_date,
                               doctor=doctor))

    # For GET request, show the form
    students = Student.query.order_by(Student.last_name, Student.first_name).all()
    return render_template('certificates/generate.html',
                          students=students,
                          today_date=datetime.now().strftime('%Y-%m-%d'))

@certificates.route('/view', methods=['GET'])
@login_required
def view_certificate():
    student_id = request.args.get('student_id')
    certificate_type = request.args.get('certificate_type')
    issue_date = request.args.get('issue_date')
    doctor = request.args.get('doctor')

    if not all([student_id, certificate_type, issue_date, doctor]):
        flash('Недостаточно данных для генерации справки', 'error')
        return redirect(url_for('certificates.generate'))

    student = Student.query.get_or_404(student_id)

    # Format the date for display
    formatted_date = datetime.strptime(issue_date, '%Y-%m-%d').strftime('%d.%m.%Y')

    return render_template('certificates/view.html',
                          student=student,
                          certificate_type=certificate_type,
                          certificate_type_name=CERTIFICATE_TYPES.get(certificate_type, 'Медицинская справка'),
                          issue_date=formatted_date,
                          doctor=doctor,
                          certificate_number=generate_certificate_number(),
                          conclusion=DEFAULT_CONCLUSIONS.get(certificate_type, 'Здоров(а).'),
                          recommendations=DEFAULT_RECOMMENDATIONS.get(certificate_type, 'Особых рекомендаций нет.'))
