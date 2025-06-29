from flask import render_template, request, redirect, url_for, jsonify
from appointmentapp import app
from appointmentapp import utils
from appointmentapp.models import *
from appointmentapp import db
from datetime import datetime


@index_bp.route('/')
def home():
    patients = utils.load_patients()
    specialties = utils.load_specialties()
    doctors = utils.load_doctors()
    return render_template('index.html', patients=patients, specialties=specialties, doctors=doctors)

@app.route('/make_appointment', methods=['POST'])
def make_appointment():
    full_name = request.form['full_name']
    date_of_birth = request.form['date_of_birth']
    address = request.form['address']
    patient_email = request.form['patient_email']
    patient_phone = request.form['patient_phone']
    insurance_number = request.form['insurance_number']
    doctor_id = int(request.form['doctor'])
    appointment_date = datetime.strptime(request.form['appointment_date'], '%Y-%m-%d')
    reason = request.form.get('reason', '')

    new_patient = Patient(
        full_name=full_name,
        date_of_birth=date_of_birth,
        address=address,
        patient_email=patient_email,
        patient_phone=patient_phone,
        insurance_number=insurance_number,
    )
    db.session.add(new_patient)
    db.session.commit()

    new_appointment = Appointment(
        patient_id=new_patient.patient_id,
        doctor_id=doctor_id,
        appointment_date=appointment_date,
        status_appointment='scheduled',
        reason=reason,
        note=''
    )
    db.session.add(new_appointment)
    db.session.commit()

    return redirect(url_for('home'))

@app.route('/appointments')
def appointments():
    # Lấy tất cả lịch hẹn, join với bác sĩ, bệnh nhân, chuyên khoa
    appointments = db.session.query(Appointment, Patient, Doctor, Specialty) \
        .join(Patient, Appointment.patient_id == Patient.patient_id) \
        .join(Doctor, Appointment.doctor_id == Doctor.doctor_id) \
        .join(Specialty, Doctor.specialty_id == Specialty.specialty_id) \
        .all()
    return render_template('appointments.html', appointments=appointments)

@app.route('/api/doctors/<int:specialty_id>')
def get_doctors_by_specialty(specialty_id):
    """API endpoint để lấy danh sách bác sĩ theo chuyên khoa"""
    doctors = Doctor.query.filter_by(specialty_id=specialty_id, doctor_status='active').all()
    return jsonify([{
        'doctor_id': doctor.doctor_id,
        'full_name': doctor.full_name
    } for doctor in doctors])

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


    
