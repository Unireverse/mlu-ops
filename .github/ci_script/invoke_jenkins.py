import os
import json
import requests
import sys
import time

if len(sys.argv) < 3:
    print("Need extra input parameters.")
    exit(-1)

localhost = "http://localhost:12345/"


os_version = "ubuntu20.04"
require_test = True
card_type = 0
pr_id = 0


for pair in sys.argv[1:]:
    print(pair)
    try:
        key, value = pair.split("=")
    except Exception as e:
        print(e)
        exit(-1)
    if key == "os":
        os_version = value
    if key == "require_test":
        require_test = bool(value)
    if key == "card_type":
        card_type = int(value)
    if key == "pr":
        pr_id = value.split("/")[2]

timestamp = str(int(time.time() * 10000))

test_infos = {
    "os_version": os_version,
    "type": "ci",
    "pr_id": pr_id,
    "timestamp": timestamp,
    "require_test": require_test
}

response = requests.post(localhost, json=test_infos)
print(response.status_code, response.text)
exit()
if response.status_code == 200:
    while 1:
        response = requests.get(localhost + "?type=10&pr_id=" + str(pr_id) + "&timestamp=" + timestamp + "&system_os=" + system_version)
        if int(json.loads(response.text)["status"]) < 200:
            time.sleep(3)
            continue
        if int(json.loads(response.text)["status"]) == 200:
            print("success")
            exit(0)
        if int(json.loads(response.text)["status"]) == 300:
            print(json.loads(response.text)["log"])
            exit(-1)
