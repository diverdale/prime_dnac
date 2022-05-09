from requests.auth import HTTPBasicAuth
import requests
import json
import typing

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

def get_power_supply_info_old(token):
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
    print(json.dumps(power_supply_details))
    return json.dumps(full_list)

def get_device_health(token):
    api_key = token
    headers = {'X-Auth-Token': api_key, 'Content-Type': 'application/json', 'Accept': 'application/json'}
    devices = requests.get(base_url + device_health_url, headers=headers, data=None, verify=False).json()
    return devices['response']


def get_power_supply_info(token) -> str:
    api_key = token
    power_supple_uri_template: str = '/dna/intent/api/v1/network-device/{device_id}/equipment?type=PowerSupply'
    headers = {'X-Auth-Token': api_key, 'Content-Type': 'application/json', 'Accept': 'application/json'}
    device_ids = get_device_ids(token)
    power_supply_details = []
    device_names = []
    device_component_map: dict[str, list[dict[str, str]]] = {}
    for device_id in device_ids:
        try:
            device_name: Optional[str] = get_device_name(token, device_id).strip("\"")
            # TODO: what do you want to do if the device name is None??
            if device_name is None:
                device_name = str(device_name)
            typing.cast(str, device_name)
            device_component_map.setdefault(str(device_name), [])

            power_supply_url: str = str(Path(
                base_url,
                power_supple_uri_template.format(device_id=device_id)
            ))
            # Below assumes successful get
            resp: list[dict[str, str]] = requests.get(power_supply_url, headers=headers, data=None, verify=False).json()
            device_component_map[device_name].extend(resp)
        except Exception:
            pass
    print(device_component_map)    
    return json.dumps(device_component_map) 


if __name__ == '__main__':
    token = get_auth_token()
    power_supply_details = get_power_supply_info(token)
    print(power_supply_details)




