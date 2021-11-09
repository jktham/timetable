import json
import requests
from datetime import datetime, timedelta

with open("credentials.json") as file:
    cred = json.load(file)
    username = cred["username"]
    password = cred["password"]
    userid = cred["userid"]

with requests.Session() as s:
    info_response = s.get("https://intranet.tam.ch/krm/timetable/classbook")

    hash = info_response.text.split("name=\"hash\" value=\"", 1)[1].split("\"", 1)[0]
    session = info_response.headers["Set-Cookie"].split("sturmsession=", 1)[1].split(";", 1)[0]

    payload = {"hash": hash, "loginschool": "krm", "loginuser": username, "loginpassword": password}
    auth_response = s.post("https://intranet.tam.ch/krm/timetable/classbook", data=payload)

    today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    monday = today - timedelta(days=today.weekday())
    sunday = today + timedelta(days=7) - timedelta(days=today.weekday())

    payload = {"startDate": monday.timestamp()*1000, "endDate": sunday.timestamp()*1000, "studentId[]": userid, "holidaysOnly": 0}
    cookies = {"username": username, "sturmuser": username, "school": "krm", "sturmsession": session}
    headers = {"x-requested-with": "XMLHttpRequest"}
    data_response = s.post("https://intranet.tam.ch/krm/timetable/ajax-get-timetable", data=payload, cookies=cookies, headers=headers)

    print(data_response.text)
    print(len(data_response.text))