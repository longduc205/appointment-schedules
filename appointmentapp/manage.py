from appointmentapp import app, db
from appointmentapp import models

if __name__ == "__main__":
    with app.app_context():
        db.drop_all()
        db.create_all()     
        print("Tables created!") 