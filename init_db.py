from app import create_app
from app.models import db
from app.models.employee import Employee
from app.models.student import Student
from app.models.medical_card import MedicalRecord
from datetime import datetime, timedelta
from app.models.sanitary_inspection import SanitaryInspection, InspectionWarning, InspectionNote
import random
from faker import Faker

fake = Faker()

app = create_app('development')

with app.app_context():
    # Create all tables
    db.create_all()

    # Create sample students
    student1 = Student(
        first_name='John',
        last_name='Doe',
        date_of_birth=datetime(2000, 1, 15),
        group="IO-123"
    )

    student2 = Student(
        first_name='Jane',
        last_name='Smith',
        date_of_birth=datetime(2001, 5, 20),
        group="IO-234"
    )

    student3 = Student(
        first_name='Michael',
        last_name='Johnson',
        date_of_birth=datetime(1999, 8, 10),
        group="IO-123"
    )

    student4 = Student(
        first_name='Emily',
        last_name='Williams',
        date_of_birth=datetime(2002, 3, 25),
        group="IO-345"
    )

    student5 = Student(
        first_name='David',
        last_name='Brown',
        date_of_birth=datetime(2001, 11, 7),
        group="IO-234"
    )

    # Add students to session
    db.session.add_all([student1, student2, student3, student4, student5])
    db.session.commit()

    # Create medical records for students with different dates

    # List of record types
    record_types = ["Простуда", "Травма", "Аллергия", "Профосмотр", "Вакцинация",
                    "Головная боль", "Консультация", "Грипп", "Ангина", "Бронхит"]

    # List of doctors
    doctors = ["Dr. Johnson", "Dr. Smith", "Dr. Williams", "Dr. Brown", "Dr. Davis",
               "Dr. Miller", "Dr. Wilson", "Dr. Moore", "Dr. Taylor", "Dr. Anderson"]

    # List of descriptions
    descriptions = [
        "Сезонная простуда. Назначены противовирусные препараты.",
        "Ушиб правого колена. Рекомендован покой.",
        "Аллергическая реакция на пыльцу. Назначены антигистаминные.",
        "Ежегодный профилактический осмотр. Патологий не выявлено.",
        "Плановая вакцинация от гриппа.",
        "Жалобы на головную боль. Рекомендован режим и анальгетики.",
        "Консультация по поводу профилактики сезонных заболеваний.",
        "Грипп. Назначено противовирусное лечение и постельный режим.",
        "Бактериальная ангина. Назначен курс антибиотиков.",
        "Острый бронхит. Назначены антибиотики и отхаркивающие средства.",
        "Растяжение связок левого голеностопа. Наложена фиксирующая повязка.",
        "Перелом указательного пальца правой руки. Наложена гипсовая лонгета.",
        "Контрольный осмотр после перелома. Заживление идет нормально.",
        "Снятие гипсовой лонгеты. Рекомендованы упражнения для разработки.",
        "Мигрень. Назначены анальгетики и консультация невролога."
    ]

    # Generate medical records
    medical_records = []

    # Current date for reference
    current_date = datetime.now()

    # For each student, create multiple records with different dates
    for student in [student1, student2, student3, student4, student5]:
        # Generate 3-7 records per student
        num_records = random.randint(3, 7)

        for i in range(num_records):
            # Generate a random date within the last year
            days_ago = random.randint(1, 365)
            record_date = current_date - timedelta(days=days_ago)

            # Select random record type, doctor, and description
            record_type = random.choice(record_types)
            doctor = random.choice(doctors)
            description = random.choice(descriptions)

            # Create the medical record
            med_record = MedicalRecord(
                student_id=student.id,
                date=record_date,
                record_type=record_type,
                description=description,
                doctor=doctor
            )

            medical_records.append(med_record)

    # Add some specific records for reporting purposes

    # Add multiple records of the same type for trend analysis
    for i in range(5):
        days_ago = random.randint(1, 30)  # Last month
        record_date = current_date - timedelta(days=days_ago)

        flu_record = MedicalRecord(
            student_id=random.choice([student1.id, student2.id, student3.id, student4.id, student5.id]),
            date=record_date,
            record_type="Грипп",
            description="Сезонный грипп. Назначено лечение.",
            doctor=random.choice(doctors)
        )

        medical_records.append(flu_record)

    # Add records for the same student on consecutive days (for follow-up visits)
    for i in range(3):
        follow_up_date = current_date - timedelta(days=i * 2 + 5)

        follow_up_record = MedicalRecord(
            student_id=student3.id,
            date=follow_up_date,
            record_type="Контроль",
            description=f"Контрольный осмотр #{i + 1}. Наблюдается положительная динамика.",
            doctor="Dr. Johnson"
        )

        medical_records.append(follow_up_record)

    # Add records for the same day (to test daily statistics)
    same_day = current_date - timedelta(days=10)
    for i in range(4):
        same_day_record = MedicalRecord(
            student_id=random.choice([student1.id, student2.id, student4.id, student5.id]),
            date=same_day,
            record_type=random.choice(record_types),
            description=random.choice(descriptions),
            doctor=random.choice(doctors)
        )

        medical_records.append(same_day_record)

    # Add some injury records for injury report testing
    for i in range(6):
        days_ago = random.randint(1, 180)  # Last 6 months
        injury_date = current_date - timedelta(days=days_ago)

        injury_record = MedicalRecord(
            student_id=random.choice([student1.id, student2.id, student3.id, student4.id, student5.id]),
            date=injury_date,
            record_type="Травма",
            description=random.choice([
                "Ушиб мягких тканей левого предплечья.",
                "Растяжение связок правого голеностопа.",
                "Ушиб правого колена при падении.",
                "Травма пальца левой руки.",
                "Спортивная травма плеча.",
                "Ушиб мягких тканей спины."
            ]),
            doctor=random.choice(doctors)
        )

        medical_records.append(injury_record)

    # Add all medical records to session
    db.session.add_all(medical_records)
    db.session.commit()

    print(
        f"Database initialized with {len([student1, student2, student3, student4, student5])} sample students and {len(medical_records)} medical records.")

    # Check if there are already employees
    if Employee.query.count() == 0:
        # Create admin user
        admin = Employee(
            username='admin',
            email='admin@example.com',
            first_name='Admin',
            last_name='User',
            position='Administrator',
            department='IT',
            hire_date=datetime.now(),
            salary=100000.00,
            is_admin=True
        )
        admin.password = 'password123'

        db.session.add_all([admin])
        db.session.commit()

        print("Database initialized with sample employees.")
    else:
        print("Database already contains employees.")


    # init sanitary inspections

    inspection_types = ['плановая', 'по_жалобе', 'повторная', 'предварительная']
    ratings = ['отлично', 'хорошо', 'удовлетворительно', 'неудовлетворительно']
    warning_categories = [
        'безопасность_пищи', 'чистота', 'оборудование', 'борьба_с_вредителями',
        'гигиена_сотрудников', 'контроль_температуры', 'хранение', 'документооборот'
    ]
    severities = ['критическое', 'значительное', 'незначительное']
    note_types = ['наблюдение', 'рекомендация', 'похвала']

    facility_types = [
        'Ресторан', 'Кафе', 'Фуд-трак', 'Продуктовый магазин', 'Пекарня',
        'Кейтеринг', 'Школьная столовая', 'Больничная кухня', 'Ресторан отеля'
    ]
    inspections = []
    num_inspections = 50

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