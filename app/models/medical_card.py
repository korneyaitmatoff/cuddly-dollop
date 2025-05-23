from datetime import datetime
from app.models import db

class MedicalRecord(db.Model):
    __tablename__ = 'medical_records'

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    date = db.Column(db.Date, default=datetime.utcnow, nullable=False)
    record_type = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    doctor = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<MedicalRecord {self.id} for Student {self.student_id}>'
