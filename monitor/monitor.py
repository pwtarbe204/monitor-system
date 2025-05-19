import sys
import time

from modules import info_monitor, net_monitor, sys_monitor, url_checker, sender
from dotenv import load_dotenv
import os
import requests

load_dotenv(verbose=True)
SERVER_IP = os.getenv("SERVER_IP")
URL = os.getenv("URL")

def main():
    sysinfo = sender.sysinfo()
    response = requests.post(f"{URL}api/sysinfo", json=sysinfo)
    traffic = sender.nettraffic()
    response = requests.post(f"{URL}api/network", json=traffic)
    try:
        data = response.json()
        print(data)
    except requests.JSONDecodeError:
        print("Lỗi: Phản hồi không phải là JSON hợp lệ")

if __name__ == "__main__":
    #data = sender.getinfo()
    #response = requests.post(f"{URL}api/addagent", json=data)
    #print(response.json())
    try:
        while True:
            main()
            time.sleep(1)
    except KeyboardInterrupt:
        sys.exit(0)
