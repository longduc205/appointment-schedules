from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from wtforms import SelectField
from appointmentapp.models import *
from appointmentapp import db

admin = Admin(name='Appointment Management', template_mode='bootstrap4')  # Không gán app ở đây

class UserModelView(ModelView):
    form_overrides = {
        'user_role': SelectField,
        'user_status': SelectField,
    }

    form_args = {
        'user_role': {
            'choices': [('admin', 'Admin'), ('doctor', 'Doctor'), ('patient', 'Patient')]
        },
        'user_status': {
            'choices': [('active', 'Active'), ('inactive', 'Inactive')]
        }
    }

class DoctorModelView(ModelView):
    form_overrides = {
        'doctor_status': SelectField,
    }
    form_args = {
        'doctor_status': {
            'choices': [
                ('active', 'Active'),
                ('inactive', 'Inactive')
            ]
        }
    }

class RoomModelView(ModelView):
    form_overrides = {
        'room_status': SelectField,
    }
    form_args = {
        'room_status': {
            'choices': [
                ('available', 'Available'),
                ('occupied', 'Occupied')
            ]
        }
    }

class AppointmentModelView(ModelView):
    form_overrides = {
        'status_appointment': SelectField,
    }
    form_args = {
        'status_appointment': {
            'choices': [
                ('scheduled', 'Scheduled'),
                ('completed', 'Completed'),
                ('cancelled', 'Cancelled')
            ]
        }
    }

class ScheduleModelView(ModelView):
    form_overrides = {
        'schedule_status': SelectField,
    }
    form_args = {
        'schedule_status': {
            'choices': [
                ('available', 'Available'),
                ('booked', 'Booked')
            ]
        }
    }

class PaymentModelView(ModelView):
    form_overrides = {
        'payment_method': SelectField,
        'payment_status': SelectField,
    }
    form_args = {
        'payment_method': {
            'choices': [
                ('cash', 'Cash'),
                ('card', 'Card'),
                ('insurance', 'Insurance'),
                ('mobile banking', 'Mobile Banking'),
                ('QR code', 'QR Code')
            ]
        },
        'payment_status': {
            'choices': [
                ('pending', 'Pending'),
                ('completed', 'Completed'),
                ('failed', 'Failed')
            ]
        }
    }

admin.add_view(UserModelView(User, db.session))
admin.add_view(ModelView(Patient, db.session))
admin.add_view(DoctorModelView(Doctor, db.session))
admin.add_view(ModelView(Specialty, db.session))
admin.add_view(RoomModelView(Room, db.session))
admin.add_view(AppointmentModelView(Appointment, db.session))
admin.add_view(ScheduleModelView(Schedule, db.session))
admin.add_view(PaymentModelView(Payment, db.session))
