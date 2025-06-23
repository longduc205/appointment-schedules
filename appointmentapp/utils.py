from appointmentapp.models import *

def load_patients():
    return Patient.query.all()

def load_doctors():
    return Doctor.query.all()

def load_specialties():
    return Specialty.query.all()

def load_rooms():
    return Room.query.all()

def load_appointments():
    return Appointment.query.all()

def load_schedules():
    return Schedule.query.all()

def load_payments():
    return Payment.query.all()

def load_users():
    return User.query.all()







