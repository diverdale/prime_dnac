
from webbrowser import get
from requests.auth import HTTPBasicAuth
import requests
import json

from urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

username = 'username'
password = 'password'

base_url = 'https://<ip address>'
auth_url = '/dna/system/api/v1/auth/token'
device_list_url = '/dna/intent/api/v1/network-device'
device_url = '/dna/intent/api/v1/device-detail'
device_health_url='/dna/intent/api/v1/device-health'


def get_auth_token():
    resp = requests.post(base_url + auth_url, auth=HTTPBasicAuth(username, password), verify=False).json()
    token = resp['Token']
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

def get_device_health(token):
    api_key = token
    headers = {'X-Auth-Token': api_key, 'Content-Type': 'application/json', 'Accept': 'application/json'}
    devices = requests.get(base_url + device_health_url, headers=headers, data=None, verify=False).json()
    return devices['response']


if __name__ == '__main__':
    token = get_auth_token()
    interfaces = get_all_interfaces(token)
    print(interfaces)




