from flask import Blueprint, render_template, session, redirect, url_for
from appointmentapp.models import db, User, Patient

user_bp = Blueprint('user_bp', __name__, url_prefix='/user')


@user_bp.route('/profile')
def login_as(user_id):
    session['user_id'] = user_id
    return redirect(url_for('user_bp.profile'))

# 🛠 THÊM route cho profile
@user_bp.route('/profile/view')  # hoặc vẫn là '/profile' nếu không trùng
def profile():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('index'))  # hoặc url_for('main_bp.login')

    user = User.query.filter_by(user_id=user_id).first()
    patient = Patient.query.filter_by(user_id=user_id).first()

    if not user or not patient:
        return "User not found", 404

    return render_template('user.html', user=user, patient=patient)


