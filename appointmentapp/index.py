from flask import render_template, request, redirect, url_for, jsonify
from appointmentapp import app
from appointmentapp import utils
from appointmentapp.models import *
from appointmentapp import db
from datetime import datetime

@app.route('/')
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

if __name__ == '__main__':
    from appointmentapp.admin import *
    app.run(debug=True)