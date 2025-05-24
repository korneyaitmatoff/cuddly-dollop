from datetime import datetime, timedelta
import random
from faker import Faker
from app.models.sanitary_inspection import SanitaryInspection, InspectionWarning, InspectionNote
from app.models import db

fake = Faker()


def generate_sanitary_inspections(num_inspections=50):
    """Generate sample sanitary inspection data"""

    inspection_types = ['routine', 'complaint', 'follow-up', 'pre-opening']
    ratings = ['excellent', 'good', 'fair', 'poor']
    warning_categories = [
        'food_safety', 'cleanliness', 'equipment', 'pest_control',
        'employee_hygiene', 'temperature_control', 'storage', 'documentation'
    ]
    severities = ['critical', 'major', 'minor']
    note_types = ['observation', 'recommendation', 'commendation']

    facility_types = [
        'Restaurant', 'Cafe', 'Food Truck', 'Grocery Store', 'Bakery',
        'Catering Service', 'School Cafeteria', 'Hospital Kitchen', 'Hotel Restaurant'
    ]

    inspections = []

    for _ in range(num_inspections):
        # Create inspection
        inspection_date = fake.date_time_between(start_date='-2y', end_date='now')
        facility_type = random.choice(facility_types)

        inspection = SanitaryInspection(
            inspection_date=inspection_date,
            inspector_name=fake.name(),
            facility_name=f"{fake.company()} {facility_type}",
            facility_address=fake.address(),
            inspection_type=random.choice(inspection_types),
            overall_rating=random.choice(ratings),
            created_at=inspection_date,
            updated_at=inspection_date
        )

        db.session.add(inspection)
        db.session.flush()  # Get the ID

        # Generate warnings (0-5 per inspection)
        num_warnings = random.randint(0, 5)
        for _ in range(num_warnings):
            warning = InspectionWarning(
                inspection_id=inspection.id,
                category=random.choice(warning_categories),
                severity=random.choice(severities),
                description=fake.paragraph(nb_sentences=2),
                corrective_action=fake.paragraph(nb_sentences=1) if random.choice([True, False]) else None,
                deadline=inspection_date + timedelta(days=random.randint(7, 30)) if random.choice(
                    [True, False]) else None,
                is_resolved=random.choice([True, False]),
                created_at=inspection_date
            )
            db.session.add(warning)

        # Generate notes (1-3 per inspection)
        num_notes = random.randint(1, 3)
        for _ in range(num_notes):
            note = InspectionNote(
                inspection_id=inspection.id,
                note_type=random.choice(note_types),
                content=fake.paragraph(nb_sentences=random.randint(1, 3)),
                created_at=inspection_date
            )
            db.session.add(note)

        inspections.append(inspection)

    db.session.commit()
    print(f"Generated {num_inspections} sanitary inspections with warnings and notes")
    return inspections


if __name__ == '__main__':
    generate_sanitary_inspections(50)
