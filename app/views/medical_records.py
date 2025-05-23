from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models import db
from app.models.student import Student
from app.models.medical_card import MedicalRecord
from datetime import datetime

medical_records = Blueprint('medical_records', __name__)


@medical_records.route('/medcards', methods=['GET'])
def index():
    search_query = request.args.get('search', '')
    student_id = request.args.get('student_id', type=int)

    # Get students list, filtered by search if provided
    if search_query:
        students = Student.query.filter(
            (Student.first_name.contains(search_query)) |
            (Student.last_name.contains(search_query))
        ).order_by(Student.last_name).all()
    else:
        students = Student.query.order_by(Student.last_name).all()

    # Get selected student and their medical records
    selected_student = None
    medical_records = []

    if student_id:
        selected_student = Student.query.get_or_404(student_id)
        medical_records = MedicalRecord.query.filter_by(student_id=student_id).order_by(MedicalRecord.date.desc()).all()

    # Format today's date for the date input default value
    today_date = datetime.utcnow().strftime('%Y-%m-%d')

    return render_template(
        'medical_records/index.html',
        students=students,
        selected_student=selected_student,
        medical_records=medical_records,
        today_date=today_date
    )


@medical_records.route('/medcards/add_record/<int:student_id>', methods=['POST'])
def add_record(student_id):
    student = Student.query.get_or_404(student_id)

    # Get form data
    record_type = request.form.get('record_type')
    date_str = request.form.get('date')
    description = request.form.get('description')
    doctor = request.form.get('doctor')

    # Validate form data
    errors = []
    if not record_type:
        errors.append('Тип записи обязателен')
    if not date_str:
        errors.append('Дата обязательна')
    if not description:
        errors.append('Описание обязательно')
    if not doctor:
        errors.append('Имя врача обязательно')

    # If there are errors, flash them and redirect back
    if errors:
        for error in errors:
            flash(error, 'danger')
        return redirect(url_for('medical_records.index', student_id=student_id))

    # Parse date
    try:
        date = datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError:
        flash('Неверный формат даты', 'danger')
        return redirect(url_for('medical_records.index', student_id=student_id))

    # Create and save the record
    record = MedicalRecord(
        student_id=student_id,
        record_type=record_type,
        date=date,
        description=description,
        doctor=doctor
    )

    db.session.add(record)
    db.session.commit()

    flash('Медицинская запись успешно добавлена', 'success')
    return redirect(url_for('medical_records.index', student_id=student_id))
