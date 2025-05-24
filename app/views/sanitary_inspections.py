from flask import Blueprint, render_template, jsonify, request, redirect, url_for, flash
from datetime import datetime
from app.models.sanitary_inspection import SanitaryInspection, InspectionWarning, InspectionNote
from app.models import db

sanitary_inspections_bp = Blueprint('sanitary_inspections', __name__)

@sanitary_inspections_bp.route('/sanitary_inspections')
@sanitary_inspections_bp.route('/sanitary_inspections/<int:inspection_id>')
def sanitary_inspections(inspection_id=None):
    """Main sanitary inspections page with sidebar listing"""
    inspections = SanitaryInspection.query.order_by(
        SanitaryInspection.inspection_date.desc()
    ).all()

    selected_inspection = None
    if inspection_id:
        selected_inspection = SanitaryInspection.query.get_or_404(inspection_id)

    return render_template('sanitary_inspections.html',
                         inspections=inspections,
                         selected_inspection=selected_inspection)

@sanitary_inspections_bp.route('/sanitary_inspections/api/<int:inspection_id>')
def get_inspection_details(inspection_id):
    """API endpoint to get detailed inspection data for AJAX requests"""
    inspection = SanitaryInspection.query.get_or_404(inspection_id)

    # Serialize the inspection data
    inspection_data = {
        'id': inspection.id,
        'facility_name': inspection.facility_name,
        'facility_address': inspection.facility_address,
        'inspection_date': inspection.inspection_date.isoformat(),
        'inspector_name': inspection.inspector_name,
        'inspection_type': inspection.inspection_type.title(),
        'overall_rating': inspection.overall_rating.title(),
        'warnings': [],
        'notes': []
    }

    # Add warnings
    for warning in inspection.warnings:
        warning_data = {
            'id': warning.id,
            'category': warning.category,
            'severity': warning.severity,
            'description': warning.description,
            'corrective_action': warning.corrective_action,
            'deadline': warning.deadline.isoformat() if warning.deadline else None,
            'is_resolved': warning.is_resolved,
            'created_at': warning.created_at.isoformat()
        }
        inspection_data['warnings'].append(warning_data)

    # Add notes
    for note in inspection.notes:
        note_data = {
            'id': note.id,
            'note_type': note.note_type,
            'content': note.content,
            'created_at': note.created_at.isoformat()
        }
        inspection_data['notes'].append(note_data)

    return jsonify(inspection_data)

@sanitary_inspections_bp.route('/sanitary_inspections/filter')
def filter_inspections():
    """Filter inspections by various criteria"""
    rating = request.args.get('rating')
    inspection_type = request.args.get('type')
    facility_name = request.args.get('facility')

    query = SanitaryInspection.query

    if rating:
        query = query.filter(SanitaryInspection.overall_rating == rating)

    if inspection_type:
        query = query.filter(SanitaryInspection.inspection_type == inspection_type)

    if facility_name:
        query = query.filter(SanitaryInspection.facility_name.ilike(f'%{facility_name}%'))

    inspections = query.order_by(SanitaryInspection.inspection_date.desc()).all()

    return render_template('sanitary_inspections.html', inspections=inspections)

@sanitary_inspections_bp.route('/sanitary_inspections/stats')
def inspection_stats():
    """Get statistics for dashboard or reports"""
    total_inspections = SanitaryInspection.query.count()

    # Count by rating
    rating_stats = db.session.query(
        SanitaryInspection.overall_rating,
        db.func.count(SanitaryInspection.id)
    ).group_by(SanitaryInspection.overall_rating).all()

    # Count by type
    type_stats = db.session.query(
        SanitaryInspection.inspection_type,
        db.func.count(SanitaryInspection.id)
    ).group_by(SanitaryInspection.inspection_type).all()

    # Count unresolved warnings
    unresolved_warnings = InspectionWarning.query.filter_by(is_resolved=False).count()

    stats = {
        'total_inspections': total_inspections,
        'rating_distribution': dict(rating_stats),
        'type_distribution': dict(type_stats),
        'unresolved_warnings': unresolved_warnings
    }

@sanitary_inspections_bp.route('/sanitary_inspections/<int:inspection_id>/add_warning', methods=['POST'])
def add_warning(inspection_id):
    """Add a new warning to an inspection"""
    inspection = SanitaryInspection.query.get_or_404(inspection_id)

    try:
        # Create new warning
        warning = InspectionWarning(
            inspection_id=inspection_id,
            category=request.form['category'],
            severity=request.form['severity'],
            description=request.form['description'],
            corrective_action=request.form.get('corrective_action', ''),
            deadline=datetime.strptime(request.form['deadline'], '%Y-%m-%d').date() if request.form.get('deadline') else None,
            is_resolved=False
        )

        db.session.add(warning)
        db.session.commit()

        flash('Нарушение успешно добавлено', 'success')

    except Exception as e:
        db.session.rollback()
        flash('Ошибка при добавлении нарушения', 'error')

    return redirect(url_for('sanitary_inspections.sanitary_inspections', inspection_id=inspection_id))

@sanitary_inspections_bp.route('/sanitary_inspections/<int:inspection_id>/add_note', methods=['POST'])
def add_note(inspection_id):
    """Add a new note to an inspection"""
    inspection = SanitaryInspection.query.get_or_404(inspection_id)

    try:
        # Create new note
        note = InspectionNote(
            inspection_id=inspection_id,
            note_type=request.form['note_type'],
            content=request.form['content'],
            created_at=datetime.now()
        )

        db.session.add(note)
        db.session.commit()

        flash('Заметка успешно добавлена', 'success')

    except Exception as e:
        db.session.rollback()
        flash('Ошибка при добавлении заметки', 'error')

    return redirect(url_for('sanitary_inspections.sanitary_inspections', inspection_id=inspection_id))

@sanitary_inspections_bp.route('/sanitary_inspections/<int:inspection_id>/toggle_warning/<int:warning_id>', methods=['POST'])
def toggle_warning_status(inspection_id, warning_id):
    """Toggle warning resolved status"""
    warning = InspectionWarning.query.get_or_404(warning_id)

    try:
        warning.is_resolved = not warning.is_resolved
        db.session.commit()

        status = 'устранено' if warning.is_resolved else 'не устранено'
        flash(f'Статус нарушения изменен на "{status}"', 'success')

    except Exception as e:
        db.session.rollback()
        flash('Ошибка при изменении статуса нарушения', 'error')

    return redirect(url_for('sanitary_inspections.sanitary_inspections', inspection_id=inspection_id))
    return jsonify(stats)
