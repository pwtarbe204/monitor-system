import socket
import platform

def getInfo():
    os = platform.system()
    hostname = socket.gethostname()
    ip = socket.gethostbyname(hostname)
    return {
        "os": os,
        "hostname": hostname,
        "ip": ip
    }