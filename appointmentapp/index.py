from flask import render_template, request, session, url_for, redirect, flash
from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from appointmentapp.models import User, Patient, Appointment
from appointmentapp.extensions import db
from appointmentapp import utils
index_bp = Blueprint('index_bp', __name__)


@index_bp.route('/')
def home():
    return render_template('login.html')


@index_bp.route('/userpatient')


def profile():
    user_id = session.get('user_id') or 1  # Lấy user_id từ session (giả định là 1 nếu chưa đăng nhập)

    user = User.query.filter_by(user_id=user_id).first()
    patient = Patient.query.filter_by(patient_id=user_id).first()

    if not user or not patient:
        return "User not found", 404

    return render_template('user.html', user=user, patient=patient)

@index_bp.route('/update-user/<int:user_id>', methods=['POST'])
def update_user_profile(user_id):
    user = User.query.get(user_id)
    patient = Patient.query.get(user_id)

    if not user or not patient:
        flash('User not found.', 'danger')
        return redirect(url_for('index_bp.profile'))

    # Lấy dữ liệu từ form một cách an toàn
    user.fullname_user = request.form.get('fullname_user')
    user.user_email = request.form.get('user_email')
    user.user_phone = request.form.get('user_phone')
    patient.address = request.form.get('address')
    patient.date_of_birth = request.form.get('date_of_birth')

    db.session.commit()
    flash('Information updated successfully!', 'success')
    return redirect(url_for('index_bp.profile'))
def update_user_profile(user_id):
    print("🧾 Dữ liệu form nhận được:", request.form)

@index_bp.route('/appointmentwatching')
def appointments():
    appointments = Appointment.query.filter(Appointment.status_appointment != 'cancelled').all()
    return render_template('appointmentwatching.html', appointments=appointments)

@index_bp.route('/cancel-appointment/<int:appointment_id>', methods=['POST'])
def cancel_appointment(appointment_id):
    appointment = Appointment.query.get(appointment_id)
    if appointment:
        if appointment.status_appointment == 'completed':
            flash('Cannot cancel a completed appointment.', 'warning')
        appointment.status_appointment = 'cancelled'
        db.session.commit()
        flash('Appointment has been cancelled.', 'success')
    else:
        flash('Appointment not found.', 'error')
    return redirect(url_for('index_bp.appointments'))

@index_bp.route('/logout')
def logout():
    
    session.clear()

    # Chuyển hướng về trang chủ hoặc đăng nhập
    return redirect(url_for('index_bp.home'))


    
