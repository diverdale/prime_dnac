from email.mime import base
import re
from webbrowser import get
from requests.auth import HTTPBasicAuth
import pprint

import urllib3
import requests
import json

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

def get_device_by_id(token, device_id):
    api_key = token
    url = base_url + device_url + "?searchBy=" + device_id + "&identifier=uuid"
    headers = {'X-Auth-Token': api_key, 'Content-Type': 'application/json', 'Accept': 'application/json'}
    device = requests.get(url, headers=headers, data=None, verify=False).json()
    return json.dumps(device['response'])

def get_device_name(token, device_id):
    api_key = token
    url = base_url + device_url + "?searchBy=" + device_id + "&identifier=uuid"
    headers = {'X-Auth-Token': api_key, 'Content-Type': 'application/json', 'Accept': 'application/json'}
    device = requests.get(url, headers=headers, data=None, verify=False).json()
    return json.dumps(device['response']['nwDeviceName'])

def get_device_ids(token):
    device_ids=[]
    api_key = token
    headers = {'X-Auth-Token': api_key, 'Content-Type': 'application/json', 'Accept': 'application/json'}
    devices = requests.get(base_url + device_list_url, headers=headers, data=None, verify=False).json()
    print(json.dumps(devices))
    for device in devices['response']:
        device_ids.append(device['id'])
    return device_ids

def get_all_interfaces(token):
    api_key = token
    phy_interfaces = []
    interface_url = "/dna/intent/api/v1/interface"
    headers = {'X-Auth-Token': api_key, 'Content-Type': 'application/json', 'Accept': 'application/json'}
    interfaces = requests.get(base_url + interface_url, headers=headers, data=None, verify=False).json()
    for interface in interfaces['response']:
        if interface['interfaceType'] == "Physical":
            phy_interfaces.append(interface)
    return json.dumps(phy_interfaces)

def get_power_supply_info(token):
    api_key = token
    url1 = '/dna/intent/api/v1/network-device/'
    url2 = '/equipment?type=PowerSupply'
    headers = {'X-Auth-Token': api_key, 'Content-Type': 'application/json', 'Accept': 'application/json'}
    device_ids = get_device_ids(token)
    power_supply_details = []
    device_names = []
    for device_id in device_ids:
        try:
            device_name = get_device_name(token, device_id).strip("\"")
            if device_name is not None:
                name_entry = '{\'devName\':' + '\'' + device_name.strip("\"") + '\''
                device_names.append(name_entry)
        
            power_supply_url = base_url + url1 + device_id + url2
            resp = requests.get(power_supply_url, headers=headers, data=None, verify=False).json()
            full_list = dict(zip(device_name,resp))
            power_supply_details.append(resp['response'])
            full_list = dict(zip(device_names,power_supply_details))
        except Exception:
            pass
    return json.dumps(full_list)

def get_device_health(token):
    api_key = token
    headers = {'X-Auth-Token': api_key, 'Content-Type': 'application/json', 'Accept': 'application/json'}
    devices = requests.get(base_url + device_health_url, headers=headers, data=None, verify=False).json()
    return devices['response']


if __name__ == '__main__':
    token = get_auth_token()
    foo = get_device_ids(token)
    # interfaces = get_all_interfaces(token)
    # print(interfaces)
    # print(power_supply_details.strip("[]"))
    # device_names = get_device_name(token,'3917ae41-5e4b-4d59-bdc4-50c019fd4c77')
    # print(device_names)
    # foo = get_power_supply_info(token)
        
    

    # print(device_ids)
    # devices = get_devices(token)
    # devices = get_device_health(token)
    # print(json.dumps(devices))




