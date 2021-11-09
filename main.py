import json
import requests

with open("credentials.json") as file:
    data = json.load(file)

    username = data["username"]
    password = data["password"]
    userid = data["userid"]

