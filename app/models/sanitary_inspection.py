from datetime import datetime
from app.models import db

class SanitaryInspection(db.Model):
    __tablename__ = 'sanitary_inspections'

    id = db.Column(db.Integer, primary_key=True)
    inspection_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    inspector_name = db.Column(db.String(100), nullable=False)
    facility_name = db.Column(db.String(200), nullable=False)
    facility_address = db.Column(db.Text, nullable=False)
    inspection_type = db.Column(db.String(50), nullable=False)  # routine, complaint, follow-up
    overall_rating = db.Column(db.String(20), nullable=False)  # excellent, good, fair, poor
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    warnings = db.relationship('InspectionWarning', backref='inspection', lazy=True, cascade='all, delete-orphan')
    notes = db.relationship('InspectionNote', backref='inspection', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<SanitaryInspection {self.facility_name} - {self.inspection_date}>'

class InspectionWarning(db.Model):
    __tablename__ = 'inspection_warnings'

    id = db.Column(db.Integer, primary_key=True)
    inspection_id = db.Column(db.Integer, db.ForeignKey('sanitary_inspections.id'), nullable=False)
    category = db.Column(db.String(100), nullable=False)  # food_safety, cleanliness, equipment, etc.
    severity = db.Column(db.String(20), nullable=False)  # critical, major, minor
    description = db.Column(db.Text, nullable=False)
    corrective_action = db.Column(db.Text)
    deadline = db.Column(db.DateTime)
    is_resolved = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<InspectionWarning {self.category} - {self.severity}>'

class InspectionNote(db.Model):
    __tablename__ = 'inspection_notes'

    id = db.Column(db.Integer, primary_key=True)
    inspection_id = db.Column(db.Integer, db.ForeignKey('sanitary_inspections.id'), nullable=False)
    note_type = db.Column(db.String(50), nullable=False)  # observation, recommendation, commendation
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<InspectionNote {self.note_type}>'
