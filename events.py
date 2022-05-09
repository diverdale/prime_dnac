from email.mime import base
from venv import create
from requests.auth import HTTPBasicAuth
import requests
import json
from argparse import ArgumentParser

from urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

username = 'admin'
password = 'RTPdnacL@B!123'

base_url = 'https://10.207.165.245'
auth_url = '/dna/system/api/v1/auth/token'
device_list_url = '/dna/intent/api/v1/network-device'
device_url = '/dna/intent/api/v1/device-detail'
device_health_url='/dna/intent/api/v1/device-health'


def get_auth_token():
    resp = requests.post(base_url + auth_url, auth=HTTPBasicAuth(username, password), verify=False).json()
    token = resp['Token']
    # insert logging here
    return token

def get_event_ids(token):
    event_ids=[]
    api_key = token
    url = "/dna/intent/api/v1/events?tags=ASSURANCE&limit=10"
    headers = {'X-Auth-Token': api_key, 'Content-Type': 'application/json', 'Accept': 'application/json'}
    resp = requests.get(base_url + url, headers=headers, data=None, verify=False).json()
    for event in resp:
        event_ids.append(event['eventId'])
    return event_ids

def get_subscriptions(token):
    api_key = token
    url = "/dna/intent/api/v1/event/subscription/rest"
    headers = {'X-Auth-Token': api_key, 'Content-Type': 'application/json', 'Accept': 'application/json'}
    resp = requests.get(base_url + url, headers=headers, data=None, verify=False).json()
    return json.dumps(resp)

def create_subscription(token, event_ids):

    events = event_ids
    api_key = token
    headers = {'X-Auth-Token': api_key, 'Content-Type': 'application/json', 'Accept': 'application/json'}
    name = "Dale"
    # eventids = get_event_ids(token)
    url = "/dna/intent/api/v1/event/subscription/rest"

    payload = [
        {
            "name": "Splunk Enterprise",
            "description": "",
            "subscriptionEndpoints": [
                {
                    "subscriptionDetails":{
                    "connectorType": "REST",
                    "name": "Splunk Enterprise",
                    "description": "",
                    "url": url,
                    "method": "POST",
                    "trustCert": True,
                    }
                }
            ],
            "filter": {
                "eventIds": []
            },
            "isPrivate": False,
        }
    ]

    response = requests.post(base_url + url, headers=headers, data=json.dumps(payload), verify=False)
    print(response.text.encode('utf-8'))

def test_args(**args):
    
    foo = args.pop('foo')
    token = args.pop('token')
    print(token)

if __name__ == "__main__":
    token = get_auth_token()
    event_ids = get_event_ids(token)
    # print(event_ids)
    sub = create_subscription(token, event_ids=event_ids)
    # print(sub)
    
    # subs = get_subscriptions(token)
    # print(subs)