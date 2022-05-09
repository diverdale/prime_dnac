import requests
import json

from urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

username = 'root'
password = 'WWmas123!'

base_url = "https://172.18.123.89"
device_url = "/webacs/api/v4/data/Devices?.full=true"

def get_devices():
    # api_key = token
    devices = []
    url = base_url + device_url
    headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
    raw_devices = requests.get(url, auth=(username, password), headers=headers, verify=False).json()
    for device in raw_devices['queryResponse']['entity']:
        devices.append(device)
    return devices

def get_cpu(device_ips):
    device_ips = device_ips
    cpu_info = []
    cpu_url = "/webacs/api/v4/op/statisticsService/device/topNCPU.json?range=1&topN=100&type=FH&source="
    headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
    for ip in device_ips:
        url = base_url + cpu_url + ip
        response = requests.get(url, auth=(username, password), headers=headers, verify=False).json()
        cpu_info.append(response)
    return cpu_info

def get_mem(device_ips):
    device_ips = device_ips
    mem_info = []
    mem_url = "/webacs/api/v4/op/statisticsService/device/topNMemory.json?range=1&topN=100&type=FH&source="
    headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
    for ip in device_ips:
        url = base_url + mem_url + ip
        response = requests.get(url, auth=(username, password), headers=headers, verify=False).json()
        mem_info.append(response)
    return mem_info

def get_temp(device_ips):
    device_ips = device_ips
    temp_info = []
    temp_url = "/webacs/api/v4/op/statisticsService/device/topNTemp.json?range=1&topN=100&type=FH&source="
    headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
    for ip in device_ips:
        url = base_url + temp_url + ip
        response = requests.get(url, auth=(username, password), headers=headers, verify=False).json()
        temp_info.append(response)
    return temp_info

if __name__ == "__main__":
    devices = get_devices()
    deviceIps = []
    for device in devices:
        # print(device['devicesDTO']['ipAddress'])
        deviceIps.append(device['devicesDTO']['ipAddress'])

    cpu_info = get_cpu(deviceIps)
    for cpu in cpu_info:
        print(cpu['mgmtResponse']['statisticsDTO'])
    
    mem_info = get_mem(deviceIps)
    for mem in mem_info:
         print(mem['mgmtResponse']['statisticsDTO'])
    
    temp_info = get_temp(deviceIps)
    for temp in temp_info:
        print(temp['mgmtResponse']['statisticsDTO'])

    
  

  
