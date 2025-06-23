from appointmentapp import app
from flask_admin import Admin
from appointmentapp.models import *
from flask_admin.contrib.sqla import ModelView
from wtforms import SelectField

admin = Admin(app, name='Appointment Management', template_mode='bootstrap4') 

class UserModelView(ModelView):
    form_overrides = {
        'user_role': SelectField,
        'user_status': SelectField,
    }

    # Cung cấp danh sách lựa chọn tương ứng
    form_args = {
        'user_role': {
            'choices': [
                ('admin', 'Admin'),
                ('doctor', 'Doctor'),
                ('patient', 'Patient'),
            ]
        },
        'user_status': {
            'choices': [
                ('active', 'Active'),
                ('inactive', 'Inactive')
            ]
        }
    }
    

admin.add_view(UserModelView(User, db.session))
admin.add_view(ModelView(Patient, db.session))
admin.add_view(ModelView(Doctor, db.session))
admin.add_view(ModelView(Specialty, db.session))
admin.add_view(ModelView(Room, db.session))
admin.add_view(ModelView(Appointment, db.session))
admin.add_view(ModelView(Schedule, db.session))
admin.add_view(ModelView(Payment, db.session))