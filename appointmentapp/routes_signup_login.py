from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from appointmentapp.models import db, User, Patient
from datetime import datetime

main_bp = Blueprint('main_bp', __name__)

@main_bp.route('/')
def home():
    return '<h2>Welcome! <a href="/signup">Sign up</a> or <a href="/login">Log in</a></h2>'

@main_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        try:
            first_name = request.form['first_name']
            last_name = request.form['last_name']
            email = request.form['email']
            password_raw = request.form['password']
            password_hashed = generate_password_hash(password_raw)
            dob = datetime.strptime(f"{request.form['year']}-{request.form['month']}-{request.form['day']}", "%Y-%m-%d")

            user = User(
                user_name=email,
                password=password_hashed,
                user_email=email,
                fullname_user=f"{first_name} {last_name}",
                user_phone="0000000000",
                user_role="patient",
                user_status="active"
            )
            db.session.add(user)
            db.session.commit()

            patient = Patient(
                full_name=f"{first_name} {last_name}",
                date_of_birth=dob,
                patient_email=email,
                patient_phone="0000000000",
                insurance_number="N/A",
                user_id=user.user_id
            )
            db.session.add(patient)
            db.session.commit()

            session['user_id'] = user.user_id  # Tự động đăng nhập sau khi đăng ký
            return redirect(url_for('user_bp.profile'))

        except Exception as e:
            db.session.rollback()
            return f"Signup error: {e}"
    return render_template('signup.html')


@main_bp.route('/login', methods=['GET', 'POST'])  # Dùng Blueprint nếu có
def login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')

        # Tìm user trong bảng User
        user = User.query.filter_by(user_name=username).first()

        if user and check_password_hash(user.password, password):
            session['user_id'] = user.user_id
            session['user_role'] = user.user_role

            # Điều hướng dựa trên user_role
            if user.user_role == 'doctor':
                session['doctor_logged_in'] = True
                session['doctor_id'] = user.user_id
                return redirect(url_for('doctor_bp.doctor_dashboard'))
            elif user.user_role == 'patient':
                return redirect(url_for('user_bp.profile'))  # hoặc appointment page

            flash("Unknown role!", "warning")
            return redirect(url_for('main_bp.login'))

        else:
            flash("Invalid username or password!", "danger")

    return render_template('login.html')

@main_bp.route('/login-doctor', methods=['GET', 'POST'])
def login_doctor():
    if request.method == 'POST':
        email = request.form.get('email')
        password_input = request.form.get('password')

        user = User.query.filter_by(user_email=email, user_role='doctor').first()

        if user and check_password_hash(user.password, password_input):
            session['user_id'] = user.user_id
            session['user_name'] = user.fullname_user
            session['role'] = user.user_role
            return redirect(url_for('user_bp.profile'))  # hoặc trang riêng cho doctor

        flash("Invalid email or password", "danger")

    return render_template('login_doctor.html')  # tạo riêng file HTML nếu muốn
