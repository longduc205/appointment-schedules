from flask import render_template, request, redirect, url_for
from appointmentapp import app
from appointmentapp import utils
from appointmentapp.models import Patient
from appointmentapp import db

@app.route('/')
def home():
    patients = utils.load_patients()
    return render_template('index.html', patients=patients)

@app.route('/make_appointment', methods=['POST'])
def make_appointment():
    full_name = request.form['full_name']
    date_of_birth = request.form['date_of_birth']
    address = request.form['address']
    patient_email = request.form['patient_email']
    patient_phone = request.form['patient_phone']
    insurance_number = request.form['insurance_number']

    new_patient = Patient(
        full_name=full_name,
        date_of_birth=date_of_birth,
        address=address,
        patient_email=patient_email,
        patient_phone=patient_phone,
        insurance_number=insurance_number
    )
    db.session.add(new_patient)
    db.session.commit()
    return redirect(url_for('home'))



if __name__ == '__main__':
    from appointmentapp.admin import *
    app.run(debug=True)