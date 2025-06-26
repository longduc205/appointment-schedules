from flask import Flask
from appointmentapp.extensions import db
from appointmentapp.routes_doctor import doctor_bp
from appointmentapp.routes_signup_login import main_bp  # đổi thành tên blueprint đúng

app = Flask(__name__)
app.secret_key = '123456'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@localhost/appointmentdb?charset=utf8mb4'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db.init_app(app)

app.register_blueprint(doctor_bp)
app.register_blueprint(main_bp)
