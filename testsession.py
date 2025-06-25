from appointmentapp import app
from flask import session, redirect, url_for

@app.route('/login-as/<int:user_id>')
def login_as(user_id):
    session['user_id'] = user_id
    return redirect(url_for('user_bp.profile'))  # nếu dùng blueprint
