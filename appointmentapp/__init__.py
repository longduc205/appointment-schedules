from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.secret_key = '123456'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@localhost/appointmentdb'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    from appointmentapp.routes_signup_login import main_bp
    from appointmentapp.user_patient import user_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(user_bp)

    return app
