from appointmentapp import app, db
from appointmentapp import models  

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        print("Tables created!")
        app.run(debug=True)

