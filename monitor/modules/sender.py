import requests
from modules import info_monitor, sys_monitor, net_monitor
from datetime import datetime
import pytz


def getinfo():
    info = info_monitor.getInfo()
    agent_name = "agent-" + info['hostname']
    hostname = info['hostname']
    host_ip = info['ip']
    os = info['os']
    status = 1
    data = {
        "agent_name": agent_name,
        "hostname": hostname,
        "host_ip": host_ip,
        "os": os,
        "status": status
    }
    return data
    #response = requests.post(f'{URL}api/addagent', json=data)

def sysinfo():
    info = getinfo()
    cpu = sys_monitor.getCpu()
    ram = sys_monitor.getRam()
    disk = sys_monitor.getDisk()
    timezone = pytz.timezone('Asia/Ho_Chi_Minh')
    timestamp = datetime.now(timezone).strftime("%Y-%m-%d %H:%M:%S")

    data = {
        "timestamp": timestamp,
        "ip": info['host_ip'],
        "cpu": cpu['usage'],
        "ram": ram['percent'],
        "disk": disk['used']
    }
    return data

def nettraffic():
    info = getinfo()
    up_down = net_monitor.getNetSpeed(interval=1)
    sent_rev = net_monitor.get_network_packets()
    data = up_down | sent_rev
    return data | {"ip": info['host_ip']}

def sendDataToServer():
    return 0



