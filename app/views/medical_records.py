from flask import Blueprint, render_template
from flask_login import login_required

medical_records_bp = Blueprint('medical_records', __name__, url_prefix='/medical-records')

@medical_records_bp.route('/')
@login_required
def index():
    """View for medical records page."""
    return render_template('medical_records/index.html', title='Медицинские карты')
