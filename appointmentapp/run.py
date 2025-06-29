from appointmentapp import create_app
from appointmentapp.admin import init_admin

app = create_app()
init_admin(app)

if __name__ == "__main__":
    app.run(debug=True)
