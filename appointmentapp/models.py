from sqlalchemy import Column, Integer, String, DateTime, Date, ForeignKey, Text, Enum, Numeric
from datetime import datetime
from sqlalchemy.orm import relationship

from appointmentapp import db


class BaseModel(db.Model):
    __abstract__ = True
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


# ----------------------------- Specialty -----------------------------
class Specialty(BaseModel):
    __tablename__ = 'Specialty'

    specialty_id = Column(Integer, primary_key=True)
    specialty_name = Column(String(50), nullable=False)
    description = Column(Text)

    # Relationships
    doctors = relationship('Doctor', back_populates='specialty')
    rooms = relationship('Room', back_populates='specialty')

    def __str__(self):
        return self.specialty_name


# ----------------------------- Room -----------------------------
class Room(BaseModel):
    __tablename__ = 'Room'

    room_id = Column(Integer, primary_key=True)
    room_number = Column(String(20), nullable=False)
    room_location = Column(String(100), nullable=False)
    room_type = Column(String(50), nullable=False)
    room_status = Column(Enum('available', 'occupied', name='room_status'), default='available')

    specialty_id = Column(Integer, ForeignKey('Specialty.specialty_id'))
    specialty = relationship('Specialty', back_populates='rooms')

    appointments = relationship('Appointment', back_populates='room')
    schedules = relationship('Schedule', back_populates='room')

    def __str__(self):
        return self.room_number


# ----------------------------- Doctor -----------------------------
class Doctor(BaseModel):
    __tablename__ = 'Doctor'

    doctor_id = Column(Integer, primary_key=True)
    full_name = Column(String(80), nullable=False)
    doctor_email = Column(String(80), nullable=False)
    doctor_phone = Column(String(15), nullable=False)
    license_number = Column(String(30), nullable=False)
    years = Column(Integer, nullable=False)
    doctor_status = Column(Enum('active', 'inactive', name='doctor_status'), default='active')

    specialty_id = Column(Integer, ForeignKey('Specialty.specialty_id'))
    specialty = relationship('Specialty', back_populates='doctors')

    appointments = relationship('Appointment', back_populates='doctor')
    schedules = relationship('Schedule', back_populates='doctor')

    def __str__(self):
        return self.full_name


# ----------------------------- Patient -----------------------------
class Patient(BaseModel):
    __tablename__ = 'Patient'

    patient_id = Column(Integer, primary_key=True)
    full_name = Column(String(30), nullable=False)
    date_of_birth = Column(Date, nullable=False)
    patient_email = Column(String(80), nullable=False)
    patient_phone = Column(String(15), nullable=False)
    address = Column(String(220))
    medical_history = Column(Text)
    insurance_number = Column(String(50), nullable=False)

    appointments = relationship('Appointment', back_populates='patient')
    payments = relationship('Payment', back_populates='patient')
    user_id = Column(Integer, ForeignKey('User.user_id'))
    user = relationship('User')
    


    def __str__(self):
        return self.full_name


# ----------------------------- User -----------------------------
class User(BaseModel):
    __tablename__ = 'User'

    user_id = Column(Integer, primary_key=True)
    user_name = Column(String(50), nullable=False)
    password = Column(String(500), nullable=False)
    user_email = Column(String(100), nullable=False)
    user_role = Column(Enum('admin', 'doctor', 'patient', name='user_role'), default='patient')
    fullname_user = Column(String(100), nullable=False)
    user_phone = Column(String(15), nullable=False)
    user_status = Column(Enum('active', 'inactive', name='user_status'), default='active')


    def __str__(self):
        return self.user_name


# ----------------------------- Appointment -----------------------------
class Appointment(BaseModel):
    __tablename__ = 'Appointment'

    appointment_id = Column(Integer, primary_key=True)

    patient_id = Column(Integer, ForeignKey('Patient.patient_id'))
    doctor_id = Column(Integer, ForeignKey('Doctor.doctor_id'))
    room_id = Column(Integer, ForeignKey('Room.room_id'))

    appointment_date = Column(DateTime, nullable=False)
    status_appointment = Column(Enum('scheduled', 'completed', 'cancelled', name='status_appointment'), default='scheduled')
    reason = Column(Text, nullable=False)
    note = Column(Text)

    # Relationships
    patient = relationship('Patient', back_populates='appointments')
    doctor = relationship('Doctor', back_populates='appointments')
    room = relationship('Room', back_populates='appointments')
    payments = relationship('Payment', back_populates='appointment')

    def __str__(self):
        return f"Appointment {self.appointment_id}"


# ----------------------------- Schedule -----------------------------
class Schedule(BaseModel):
    __tablename__ = 'Schedule'

    schedule_id = Column(Integer, primary_key=True)
    doctor_id = Column(Integer, ForeignKey('Doctor.doctor_id'))
    room_id = Column(Integer, ForeignKey('Room.room_id'))

    start = Column(DateTime, nullable=False)
    end = Column(DateTime, nullable=False)
    day = Column(Date, nullable=False)
    schedule_status = Column(Enum('available', 'booked', name='schedule_status'), default='available')

    doctor = relationship('Doctor', back_populates='schedules')
    room = relationship('Room', back_populates='schedules')

    def __str__(self):
        return f"Schedule {self.schedule_id}"


# ----------------------------- Payment -----------------------------
class Payment(BaseModel):
    __tablename__ = 'Payment'

    payment_id = Column(Integer, primary_key=True)
    appointment_id = Column(Integer, ForeignKey('Appointment.appointment_id'))
    patient_id = Column(Integer, ForeignKey('Patient.patient_id'))

    amount = Column(Numeric(10, 2), nullable=False)
    payment_method = Column(Enum('cash', 'card', 'insurance', 'mobile banking', 'QR code', name='payment_method'), nullable=False)
    payment_status = Column(Enum('pending', 'completed', 'failed', name='payment_status'), default='pending')
    payment_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    transaction_id = Column(String(100))

    appointment = relationship('Appointment', back_populates='payments')
    patient = relationship('Patient', back_populates='payments')
    

    def __str__(self):
        return f"Payment {self.payment_id}"


