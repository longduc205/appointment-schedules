from flask import Blueprint, render_template, request, redirect, session, url_for, flash
from datetime import datetime
from appointmentapp.extensions import db
from appointmentapp.models import Doctor, Schedule, Appointment, Patient

doctor_bp = Blueprint('doctor_bp', __name__)

# --- Login ---
@doctor_bp.route('/doctor/login', methods=['GET', 'POST'])
def doctor_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        doctor = Doctor.query.filter_by(username=username, password=password).first()
        if doctor:
            session['doctor_logged_in'] = True
            session['doctor_id'] = doctor.doctor_id
            return redirect(url_for('doctor_bp.doctor_dashboard'))
        else:
            flash("Invalid credentials!", "danger")

    return render_template('doctor_login.html')

# --- Register ---
@doctor_bp.route('/doctor/regester', methods=['GET', 'POST'])
def doctor_regester():
    if request.method == 'POST':
        full_name = request.form.get('full_name', '').strip()
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        confirm_password = request.form.get('confirm_password', '').strip()
        email = request.form.get('email', '').strip()
        doctor_phone = request.form.get('doctor_phone', '').strip()
        license_number = request.form.get('license_number', '').strip()

        

        if password != confirm_password:
            flash("Passwords do not match!", "danger")
            return render_template('doctor_regester.html')

        if Doctor.query.filter_by(username=username).first():
            flash("Username already exists!", "danger")
            return render_template('doctor_regester.html')

        new_doctor = Doctor(
            full_name=full_name,
            username=username,
            password=password,
            doctor_email=email,
            doctor_phone=doctor_phone,
            license_number = license_number,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )

        db.session.add(new_doctor)
        db.session.commit()

        flash("Registration successful! Please log in.", "success")
        return redirect(url_for('doctor_bp.doctor_login'))

    return render_template('doctor_regester.html')

# --- Dashboard ---
@doctor_bp.route('/doctor/dashboard')
def doctor_dashboard():
    if not session.get('doctor_logged_in'):
        return redirect(url_for('doctor_bp.doctor_login'))

    doctor_id = session.get('doctor_id')
    doctor = Doctor.query.get(doctor_id)
    schedules = Schedule.query.filter_by(doctor_id=doctor_id).all()

    return render_template('doctor_schedule.html', doctor=doctor, schedules=schedules)

# --- View appointments ---
@doctor_bp.route('/doctor/appointments')
def view_appointments():
    if not session.get('doctor_logged_in'):
        return redirect(url_for('doctor_bp.doctor_login'))

    doctor_id = session.get('doctor_id')
    appointments = Appointment.query.filter_by(doctor_id=doctor_id).all()

    return render_template('doctor_appointments.html', appointments=appointments)

# --- Accept / Reject appointment ---
@doctor_bp.route('/doctor/appointment/<int:appointment_id>/<action>')
def manage_appointment(appointment_id, action):
    if not session.get('doctor_logged_in'):
        return redirect(url_for('doctor_bp.doctor_login'))
    return f"Appointment {appointment_id} has been {action}"
