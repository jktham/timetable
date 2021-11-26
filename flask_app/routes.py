from flask_app import app
from flask import render_template, request
import timetable as tt

@app.route('/')
@app.route('/index')
def index():
    return render_template(
        'index.html', 
        data=tt.setPositionIndex(tt.getTimetable(tt.username, tt.password, tt.userid, request.args.get("week"))), 
        username=tt.username, 
        userid=tt.userid
    )