from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from app.models import db
from app.models.medical_card import MedicalRecord
from app.models.student import Student
from sqlalchemy import func, desc
from datetime import datetime, timedelta
import calendar

reports = Blueprint('reports', __name__, url_prefix='/reports')

# Helper function to calculate date ranges based on period
def get_date_range(period, start_date=None, end_date=None):
    today = datetime.now().date()

    if period == 'week':
        start = today - timedelta(days=today.weekday())
        end = start + timedelta(days=6)
        return start, end, f"Неделя ({start.strftime('%d.%m.%Y')} - {end.strftime('%d.%m.%Y')})"

    elif period == 'month':
        start = today.replace(day=1)
        last_day = calendar.monthrange(today.year, today.month)[1]
        end = today.replace(day=last_day)
        return start, end, f"Месяц ({start.strftime('%d.%m.%Y')} - {end.strftime('%d.%m.%Y')})"

    elif period == 'quarter':
        current_quarter = (today.month - 1) // 3 + 1
        start_month = (current_quarter - 1) * 3 + 1
        end_month = current_quarter * 3
        start = today.replace(month=start_month, day=1)
        end = today.replace(month=end_month, day=calendar.monthrange(today.year, end_month)[1])
        return start, end, f"Квартал ({start.strftime('%d.%m.%Y')} - {end.strftime('%d.%m.%Y')})"

    elif period == 'year':
        start = today.replace(month=1, day=1)
        end = today.replace(month=12, day=31)
        return start, end, f"Год ({start.strftime('%d.%m.%Y')} - {end.strftime('%d.%m.%Y')})"

    elif period == 'custom' and start_date and end_date:
        start = datetime.strptime(start_date, '%Y-%m-%d').date()
        end = datetime.strptime(end_date, '%Y-%m-%d').date()
        return start, end, f"Период ({start.strftime('%d.%m.%Y')} - {end.strftime('%d.%m.%Y')})"

    # Default to last 30 days if something goes wrong
    start = today - timedelta(days=30)
    return start, today, f"Последние 30 дней ({start.strftime('%d.%m.%Y')} - {today.strftime('%d.%m.%Y')})"

# Dictionary mapping report types to their titles and descriptions
REPORT_TYPES = {
    'treatment_count': {
        'title': 'Отчет по количеству обращений',
        'description': 'Данный отчет показывает общее количество обращений студентов за медицинской помощью в выбранный период.'
    },
    'injury_count': {
        'title': 'Отчет по количеству травм',
        'description': 'Данный отчет показывает количество травм, полученных студентами в выбранный период.'
    },
    'illness_distribution': {
        'title': 'Распределение заболеваний',
        'description': 'Данный отчет показывает распределение различных типов заболеваний среди студентов в выбранный период.'
    },
    'student_visits': {
        'title': 'Частота обращений студентов',
        'description': 'Данный отчет показывает студентов с наибольшим количеством обращений за медицинской помощью в выбранный период.'
    },
    'doctor_workload': {
        'title': 'Нагрузка на врачей',
        'description': 'Данный отчет показывает распределение нагрузки на врачей по количеству принятых пациентов в выбранный период.'
    }
}

@reports.route('/generate', methods=['GET', 'POST'])
@login_required
def generate():
    if request.method == 'POST':
        report_type = request.form.get('report_type')
        period = request.form.get('period')
        start_date = request.form.get('start_date')
        end_date = request.form.get('end_date')

        if not report_type or not period:
            flash('Пожалуйста, выберите тип отчета и период', 'error')
            return redirect(url_for('reports.generate'))

        if period == 'custom' and (not start_date or not end_date):
            flash('Для произвольного периода необходимо указать даты начала и окончания', 'error')
            return redirect(url_for('reports.generate'))

        # Redirect to the report view page with parameters
        return redirect(url_for('reports.view_report',
                               report_type=report_type,
                               period=period,
                               start_date=start_date,
                               end_date=end_date))

    # For GET request, show the form
    return render_template('reports/generate.html',
                          today_date=datetime.now().strftime('%Y-%m-%d'))


@reports.route('/view', methods=['GET'])
@login_required
def view_report():
    report_type = request.args.get('report_type')
    period = request.args.get('period')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    if not report_type or not period:
        flash('Недостаточно данных для формирования отчета', 'error')
        return redirect(url_for('reports.generate'))

    # Get date range based on period
    start, end, period_display = get_date_range(period, start_date, end_date)

    # Get report info
    report_info = REPORT_TYPES.get(report_type, {
        'title': 'Отчет',
        'description': 'Данные отчета'
    })

    # Initialize variables for report data
    report_data = []
    report_headers = []
    chart_data = None

    # Generate report based on type
    if report_type == 'treatment_count':
        # Query to count treatments by date
        results = db.session.query(
            func.date(MedicalRecord.date).label('date'),
            func.count(MedicalRecord.id).label('count')
        ).filter(
            MedicalRecord.date >= start,
            MedicalRecord.date <= end
        ).group_by(
            func.date(MedicalRecord.date)
        ).order_by(
            func.date(MedicalRecord.date)
        ).all()

        # Prepare data for display
        report_headers = ['Дата', 'Количество обращений']
        report_data = [(row.date.strftime('%d.%m.%Y'), row.count) for row in results]

        # Prepare chart data
        chart_data = {
            'type': 'line',
            'label': 'Количество обращений',
            'labels': [row[0] for row in report_data],
            'data': [row[1] for row in report_data],
            'borderColor': 'rgba(75, 192, 192, 1)',
            'backgroundColor': 'rgba(75, 192, 192, 0.2)'
        }

    elif report_type == 'injury_count':
        # Query to count injuries
        results = db.session.query(
            func.date(MedicalRecord.date).label('date'),
            func.count(MedicalRecord.id).label('count')
        ).filter(
            MedicalRecord.date >= start,
            MedicalRecord.date <= end,
            MedicalRecord.record_type.ilike('%травм%')  # Assuming injuries have "травм" in their type
        ).group_by(
            func.date(MedicalRecord.date)
        ).order_by(
            func.date(MedicalRecord.date)
        ).all()

        # Prepare data for display
        report_headers = ['Дата', 'Количество травм']
        report_data = [(row.date.strftime('%d.%m.%Y'), row.count) for row in results]

        # Prepare chart data
        chart_data = {
            'type': 'bar',
            'label': 'Количество травм',
            'labels': [row[0] for row in report_data],
            'data': [row[1] for row in report_data],
            'borderColor': 'rgba(255, 99, 132, 1)',
            'backgroundColor': 'rgba(255, 99, 132, 0.2)'
        }

    elif report_type == 'illness_distribution':
        # Query to count records by type
        results = db.session.query(
            MedicalRecord.record_type,
            func.count(MedicalRecord.id).label('count')
        ).filter(
            MedicalRecord.date >= start,
            MedicalRecord.date <= end
        ).group_by(
            MedicalRecord.record_type
        ).order_by(
            desc('count')
        ).all()

        # Prepare data for display
        report_headers = ['Тип заболевания', 'Количество случаев']
        report_data = [(row.record_type, row.count) for row in results]

        # Prepare chart data
        chart_data = {
            'type': 'pie',
            'label': 'Распределение заболеваний',
            'labels': [row[0] for row in report_data],
            'data': [row[1] for row in report_data]
        }

    elif report_type == 'student_visits':
        # Query to count visits by student
        results = db.session.query(
            Student.last_name,
            Student.first_name,
            func.count(MedicalRecord.id).label('count')
        ).join(
            MedicalRecord, MedicalRecord.student_id == Student.id
        ).filter(
            MedicalRecord.date >= start,
            MedicalRecord.date <= end
        ).group_by(
            Student.id
        ).order_by(
            desc('count')
        ).limit(10).all()

        # Prepare data for display
        report_headers = ['Фамилия', 'Имя', 'Количество обращений']
        report_data = [(row.last_name, row.first_name, row.count) for row in results]

        # Prepare chart data
        chart_data = {
            'type': 'bar',
            'label': 'Количество обращений',
            'labels': [f"{row[0]} {row[1]}" for row in report_data],
            'data': [row[2] for row in report_data],
            'borderColor': 'rgba(54, 162, 235, 1)',
            'backgroundColor': 'rgba(54, 162, 235, 0.2)'
        }

    elif report_type == 'doctor_workload':
        # Query to count records by doctor
        results = db.session.query(
            MedicalRecord.doctor,
            func.count(MedicalRecord.id).label('count')
        ).filter(
            MedicalRecord.date >= start,
            MedicalRecord.date <= end
        ).group_by(
            MedicalRecord.doctor
        ).order_by(
            desc('count')
        ).all()

        # Prepare data for display
        report_headers = ['Врач', 'Количество приемов']
        report_data = [(row.doctor, row.count) for row in results]

        # Prepare chart data
        chart_data = {
            'type': 'bar',
            'label': 'Нагрузка на врачей',
            'labels': [row[0] for row in report_data],
            'data': [row[1] for row in report_data],
            'borderColor': 'rgba(153, 102, 255, 1)',
            'backgroundColor': 'rgba(153, 102, 255, 0.2)'
        }

    return render_template('reports/view.html',
                           report_title=report_info['title'],
                           report_description=report_info['description'],
                           period_display=period_display,
                           report_headers=report_headers,
                           report_data=report_data,
                           chart_data=chart_data)
