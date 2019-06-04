#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable-msg=C0103, C0111

import sys
import requests
import json

with open(sys.argv[1], "r") as f:
    cred = json.load(f)

data = {
    "grant_type": "client_credentials",
    "client_id": cred["appId"],
    "client_secret": cred["password"],
    "resource": "https://management.azure.com",
}

headers = {"Content-Type": "application/x-www-form-urlencoded"}

r = requests.post(
    "https://login.windows.net/{}/oauth2/token".format(cred["tenant"]),
    data=data,
    headers=headers,
)

sys.stderr.write("Status Code:{}\n".format(r.status_code))
# print(r.text.encode("utf-8"))
print(r.text)
