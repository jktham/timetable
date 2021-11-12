from flask_app import app
from flask import render_template
import timetable

@app.route('/')
@app.route('/index')
def index():
    return render_template(
        'index.html', 
        data=timetable.data, 
        username=timetable.username, 
        userid=timetable.userid
    )