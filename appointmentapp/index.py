from flask import render_template, request, session, url_for, redirect
from appointmentapp import app
from appointmentapp import utils


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/userpatient')


def profile():
    user_id = session.get('user_id') or 1  # Lấy user_id từ session (giả định là 1 nếu chưa đăng nhập)

    user = User.query.filter_by(user_id=user_id).first()
    patient = Patient.query.filter_by(patient_id=user_id).first()

    if not user or not patient:
        return "User not found", 404

    return render_template('user.html', user=user, patient=patient)

if __name__ == '__main__':
    from appointmentapp.admin import *
    app.run(debug=True)
    
