from flask import Flask, render_template, request, redirect, session, url_for, flash
from appointmentapp import create_app, db
from appointmentapp.models import User, Patient
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash


app = create_app()

@app.route('/')
def home():
    return '<h2>This is the home page. Go to <a href="/signup">Sign up</a></h2>'


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        try:
            first_name = request.form['first_name']
            last_name = request.form['last_name']
            email = request.form['email']
            password = generate_password_hash(request.form['password'])

            dob = datetime.strptime(f"{request.form['year']}-{request.form['month']}-{request.form['day']}", "%Y-%m-%d")

           # Tạo user
            user = User(
                user_name=email,
                password=generate_password_hash(password),
                user_email=email,
                fullname_user=f"{first_name} {last_name}",
                user_phone="0000000000",
                user_role="patient",
                user_status="active"
            )
            db.session.add(user)
            db.session.commit()

            # Tạo patient gắn với user
            patient = Patient(
                full_name=f"{first_name} {last_name}",
                date_of_birth=dob,
                patient_email=email,
                patient_phone="0000000000",
                insurance_number="N/A",
                user_id=user.user_id  # ✅ Gắn khóa ngoại
            )
            db.session.add(patient)
            db.session.commit()


            return redirect('/login')
        except Exception as e:
            db.session.rollback()
            return f"Signup error: {e}"
        print(" Rendering signup.html")        
    return render_template("signup.html")

app = create_app()
app.secret_key = '123456'  # nên dùng biến môi trường ở production

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password_input = request.form.get('password')

        user = User.query.filter_by(user_email=email).first()

        if user and check_password_hash(user.password, password_input):
            # Đăng nhập thành công
            session['user_id'] = user.user_id
            session['user_name'] = user.fullname_user
            session['role'] = user.user_role

            return redirect(url_for('home'))  # hoặc bất kỳ trang nào
        else:
            flash("Invalid email or password", "danger")

    return render_template('login.html')    


if __name__ == '__main__':
    app.run(debug=True)
