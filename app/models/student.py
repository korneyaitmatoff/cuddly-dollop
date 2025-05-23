from datetime import datetime
from app.models import db


class Student(db.Model):
    __tablename__ = 'students'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    group = db.Column(db.String(50))
    date_of_birth = db.Column(db.Date)

    # Relationship with medical records
    medical_records = db.relationship('MedicalRecord', backref='student', lazy='dynamic')

    def __repr__(self):
        return f'<Student {self.last_name} {self.first_name}>'
