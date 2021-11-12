import json
import requests
from datetime import datetime, timedelta
from flask_app import app

def get_timetable(username, password, userid):
    with requests.Session() as s:
        info_response = s.get("https://intranet.tam.ch/krm/timetable/classbook")

        hash = info_response.text.split("name=\"hash\" value=\"", 1)[1].split("\"", 1)[0]
        session = info_response.headers["Set-Cookie"].split("sturmsession=", 1)[1].split(";", 1)[0]

        payload = {"hash": hash, "loginschool": "krm", "loginuser": username, "loginpassword": password}
        auth_response = s.post("https://intranet.tam.ch/krm/timetable/classbook", data=payload)
        if "userId" in auth_response.text:
            print("authentication successful")
            print("got userid: " + auth_response.text.split("userId = \"", 1)[1].split("\"", 1)[0])
            print("def userid: " + userid)
        else:
            print("authentication failed")
            return 0
            
        today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        monday = today - timedelta(days=today.weekday())
        sunday = today + timedelta(days=6) - timedelta(days=today.weekday())

        payload = {"startDate": monday.timestamp()*1000, "endDate": sunday.timestamp()*1000, "studentId[]": userid, "holidaysOnly": 0}
        cookies = {"username": username, "sturmuser": username, "school": "krm", "sturmsession": session}
        headers = {"x-requested-with": "XMLHttpRequest"}
        data_response = s.post("https://intranet.tam.ch/krm/timetable/ajax-get-timetable", data=payload, cookies=cookies, headers=headers)
        
    return data_response.json()["data"]

with open("credentials.json") as file:
    cred = json.load(file)
    username = cred["username"]
    password = cred["password"]
    userid = cred["userid"]

data = get_timetable(username, password, userid)
