import json
import requests
from datetime import datetime, timedelta

with open("credentials.json") as file:
    data = json.load(file)
    username = data["username"]
    password = data["password"]
    userid = data["userid"]

with requests.Session() as s:
    info_response = s.get("https://intranet.tam.ch/krm/timetable/classbook")

    hash = info_response.text
    hash = hash.split("name=\"hash\" value=\"", 1)[1]
    hash = hash.split("\"", 1)[0]

    session = info_response.headers["Set-Cookie"]
    session = session.split("sturmsession=", 1)[1]
    session = session.split(";", 1)[0]

    data = {"hash": hash, "loginschool": "krm", "loginuser": username, "loginpassword": password}
    auth_response = s.post("https://intranet.tam.ch/krm/timetable/classbook", data=data)

    today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    monday = today - timedelta(days=today.weekday())
    sunday = today + timedelta(days=7) - timedelta(days=today.weekday())

    data = {"startDate": monday.timestamp()*1000, "endDate": sunday.timestamp()*1000, "studentId[]": userid, "holidaysOnly": 0}
    cookies = {"username": username, "sturmuser": username, "school": "krm", "sturmsession": session}
    headers = {"x-requested-with": "XMLHttpRequest"}
    data_response = s.post("https://intranet.tam.ch/krm/timetable/ajax-get-timetable", data=data, cookies=cookies, headers=headers)

    print(data_response.text)
    print(len(data_response.text))