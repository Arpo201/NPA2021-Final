import json
import requests
import time
requests.packages.urllib3.disable_warnings()


def main():
    access_token = 'YjgzYjMzM2UtZTYwMS00ZDg0LTkwMjUtMWU5ZjZlYTZmNTg4ZDUzMTNhMWItY2Rl_P0A1_4a252141-f787-4173-a4c9-bde69c553a24'
    room_id = 'Y2lzY29zcGFyazovL3VzL1JPT00vNjUwODkzMjAtY2QxOS0xMWVjLWE1NGUtNGQ2MmNhMWM4YmVl'
    intStatus = getIntStatus()
    verifyWebexMsg(intStatus, access_token, room_id)

def getIntStatus():
    ####################################
    #3.3.1
    ####################################
    api_url = "https://10.0.15.111/restconf/data/ietf-interfaces:interfaces-state/interface=Loopback62070174"

    headers = { "Accept": "application/yang-data+json", 
                "Content-type":"application/yang-data+json"
            }

    basicauth = ("admin", "cisco")
    resp = requests.get(api_url, auth=basicauth, headers=headers, verify=False)
    # print(json.dumps(response_json, indent=4))

    if 200 == resp.status_code:
        response_json = resp.json()
        if "up" == response_json['ietf-interfaces:interface']['oper-status']:
            return 1
    return 0

def verifyWebexMsg(int_status, access_token, room_id):
    ####################################
    #3.3.2
    ####################################
    url = 'https://webexapis.com/v1/messages'
    headers = {
    'Authorization': 'Bearer {}'.format(access_token)

    }
    params = {
        'roomId': room_id
    }
    res = requests.get(url, headers=headers, params=params)
    response_json = res.json()
    intStatus = "Loopback62070174 - Operational status is down"
    if int_status:
        intStatus = "Loopback62070174 - Operational status is up"
    else:
        intStatus = "Loopback62070174 - Operational status is down"
    if len(response_json["items"]) != 0:
        if response_json["items"][0]["text"] == "62070174":
            params = {
                'roomId': room_id,
                'text': intStatus
            }
            res = requests.post(url, headers=headers, json=params)
            if not int_status:
                fixInt()
                int_status = getIntStatus()
                if int_status:
                    intStatus = "Enable Loopback62070174 - Now the Operational status is up again"
                else:
                    intStatus = "Enable Loopback62070174 - Now the Operational status is still down"
                params = {
                    'roomId': room_id,
                    'text': intStatus
                }
                res = requests.post(url, headers=headers, json=params)
        print("Received message: " + response_json["items"][0]["text"])

def fixInt():

    api_url = "https://10.0.15.111/restconf/data/ietf-interfaces:interfaces/interface=Loopback62070174"

    headers = {"Accept": "application/yang-data+json",
            "Content-type": "application/yang-data+json"
            }
    basicauth = ("admin", "cisco")

    yangConfig = {
        "ietf-interfaces:interface": {
            "name": "Loopback62070174",
            "description": "This is Loopback62070174",
            "type": "iana-if-type:softwareLoopback",
            "enabled": True,
            "ietf-ip:ipv4": {
                "address": [
                    {
                        "ip": "192.168.1.1",
                        "netmask": "255.255.255.0"
                    }
                ]
            },
            "ietf-ip:ipv6": {}
        }
    }

    resp = requests.put(api_url, data=json.dumps(yangConfig),
                        auth=basicauth, headers=headers, verify=False)


while True:
    main()
    time.sleep(1)
# print(getIntStatus())