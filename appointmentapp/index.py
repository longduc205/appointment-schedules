from flask import render_template, request
from appointmentapp import app
from appointmentapp import utils

@app.route('/')
def home():
    return render_template('index.html')


if __name__ == '__main__':
    from appointmentapp.admin import *
    app.run(debug=True)