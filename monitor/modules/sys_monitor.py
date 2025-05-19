import psutil
from modules import info_monitor

def getCpu():
    usage = psutil.cpu_percent(interval=1)
    return {
        "usage": usage
    }
def getRam():
    mem =  psutil.virtual_memory()
    return {
        "total": mem.total,
        "available": mem.available,
        "used": mem.used,
        "percent": mem.percent,
        "free": mem.free
    }
def getDisk():
    info = info_monitor.getInfo()
    if info['os'] == 'Windows':
        used =  psutil.disk_usage('C:\\').percent
        return {
            "used": used,
        }
    used =  psutil.disk_usage('/').percent
    return {
        "used": used,
        "free": f"{100 - used}.1f"
    }
