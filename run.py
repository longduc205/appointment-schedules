from appointmentapp import create_app

app = create_app()

if __name__ == '__main__':
    from appointmentapp.admin import *
    app.run(debug=True)
