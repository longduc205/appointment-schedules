from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# ✅ Tạo db trước
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.secret_key = '123456'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@localhost/appointmentdb'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # ✅ Khởi tạo app cho db
    db.init_app(app)

    # ✅ Import models SAU khi db đã init_app
    from appointmentapp import models

    # ✅ Import blueprint SAU models
    from appointmentapp.routes_signup_login import main_bp
    from appointmentapp.user_patient import user_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(user_bp)

    return app
