from flask import Flask
from appointmentapp.extensions import db
from appointmentapp.routes_doctor import doctor_bp
from appointmentapp.routes_signup_login import main_bp
from appointmentapp.user_patient import user_bp
from appointmentapp.admin import init_admin

def create_app():
    app = Flask(__name__)
    app.secret_key = '123456'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@localhost/appointmentdb?charset=utf8mb4'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

    db.init_app(app)
    init_admin(app)

    app.register_blueprint(doctor_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(user_bp)

    return app
