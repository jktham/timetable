import json
import requests
import datetime
from flask_app import app

def getTimetable(username, password, userid, weekoffset):
    if weekoffset == None:
        weekoffset = 0
    else:
        weekoffset = int(weekoffset)
    
    with requests.Session() as s:
        info_response = s.get("https://intranet.tam.ch/krm/timetable/classbook")

        hash = info_response.text.split("name=\"hash\" value=\"", 1)[1].split("\"", 1)[0]
        session = info_response.headers["Set-Cookie"].split("sturmsession=", 1)[1].split(";", 1)[0]

        payload = {"hash": hash, "loginschool": "krm", "loginuser": username, "loginpassword": password}
        auth_response = s.post("https://intranet.tam.ch/krm/timetable/classbook", data=payload)
        if userid == "":
            userid = auth_response.text.split("userId = \"", 1)[1].split("\"", 1)[0]
        if "userId" in auth_response.text:
            print("authentication successful (" + str(userid) + ")")
        else:
            print("authentication failed")
            return 0
            
        today = datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) + datetime.timedelta(weeks=weekoffset)
        start = today - datetime.timedelta(days=today.weekday())
        end = today + datetime.timedelta(days=6) - datetime.timedelta(days=today.weekday())

        payload = {"startDate": start.timestamp()*1000, "endDate": end.timestamp()*1000, "studentId[]": userid, "holidaysOnly": 0}
        cookies = {"username": username, "sturmuser": username, "school": "krm", "sturmsession": session}
        headers = {"x-requested-with": "XMLHttpRequest"}
        data_response = s.post("https://intranet.tam.ch/krm/timetable/ajax-get-timetable", data=payload, cookies=cookies, headers=headers)
    return data_response.json()["data"]

def setPositionIndex(data):
    for i in range(len(data)):
        data[i]["positionIndex"] = [datetime.datetime.utcfromtimestamp(int(data[i]["start"][6:16])).weekday() + 1, int(datetime.datetime.utcfromtimestamp(int(data[i]["start"][6:16])).strftime("%H")) - 7 + 3]
    return data

with open("credentials.json") as file:
    cred = json.load(file)
    username = cred["username"]
    password = cred["password"]
    userid = cred["userid"]

# data = setPositionIndex(getTimetable(username, password, userid, 0))
