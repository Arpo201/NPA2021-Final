import json
import requests
import time
requests.packages.urllib3.disable_warnings()


def main():
    access_token = 'MzBmNWJkODItZDhmNy00Zjg4LTg0YmMtN2Y4ZjcxM2I3MThhMzYwYzljOGYtOTQ2_P0A1_4a252141-f787-4173-a4c9-bde69c553a24'
    room_id = 'Y2lzY29zcGFyazovL3VzL1JPT00vNjUwODkzMjAtY2QxOS0xMWVjLWE1NGUtNGQ2MmNhMWM4YmVl'
    verifyWebexMsg(getIntStatus(), access_token, room_id)

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
        int_status = "Loopback62070174 - Operational status is " + response_json['ietf-interfaces:interface']['oper-status']
    else:
        int_status = "Loopback62070174 - Operational status is down"
    return int_status

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

    if len(response_json["items"]) != 0:
        if response_json["items"][0]["text"] == "62070174":
            params = {
                'roomId': room_id,
                'text': int_status
            }
            res = requests.post(url, headers=headers, json=params)
        print("Received message: " + response_json["items"][0]["text"])


while True:
    main()
    time.sleep(1)