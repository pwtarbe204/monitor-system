import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config import db
from flask import jsonify
import random

conn = db.connect()
cursor = conn.cursor()

def addGroupHost(group_name, location):
    query = 'insert into group_host values (?,?)'
    cursor.execute(query, (group_name, location, ))
    conn.commit()

def addNetTraffic(data, agent_id):
    query = 'insert into net_traffic values (?, ?, ?, ?, ?, ?)'
    cursor.execute(query, (data['timestamp'], data['sent_speed'], data['recv_speed'], data['packet_sent'], data['packet_recv'], agent_id))
    conn.commit()

def addSysInfo(data, agent_id):
    query = 'insert into sysinfo values (?, ?, ?, ?, ?)'
    cursor.execute(query, (data['timestamp'], data['cpu'], data['ram'], data['disk'], agent_id))
    conn.commit()

def addAgent(data):
    query = 'insert into agents (agent_name, hostname, host_ip, os, agent_status) values (?, ?, ?, ?, ?)'
    cursor.execute(query, (data['agent_name'], data['hostname'], data['host_ip'], data['os'], data['status'], ))
    conn.commit()

def addAgentIntoGroup(group_id, agent_id):
    query = 'update agents set group_id = ? where agent_id = ?'
    cursor.execute(query, (group_id, agent_id))
    conn.commit()

def getNetTraffic(agent_id):
    query = 'select * from net_traffic where agent_id = ?'
    cursor.execute(query, (agent_id))
    data = cursor.fetchall()
    return {
        "id": [i[0] for i in data],
        "time": [i[1] for i in data],
        "upload": [i[2] for i in data],
        "download": [i[3] for i in data],
        "packet_sent": [i[4] for i in data],
        "packet_recv": [i[5] for i in data]
    }
def getGroupHost():
    query = 'select * from group_host'
    cursor.execute(query)
    data = cursor.fetchall()
    return {
        "id": [i[0] for i in data],
        "group_name": [i[1] for i in data],
        "location": [i[2] for i in data]
    }
def getAgents():
    query = 'select * from agents'
    cursor.execute(query)
    result = cursor.fetchall()

    return {
        "id": [r[0] for r in result],
        "agent-name": [r[1] for r in result],
        "hostname": [r[2] for r in result],
        "ip": [r[3] for r in result],
        "os": [r[4] for r in result],
        "status": [r[5] for r in result],
        "group_id": [r[6] for r in result]
    }
def getAgentById(agent_id):
    query = 'select * from agents where agent_id = ?'
    cursor.execute(query, (agent_id,))
    result = cursor.fetchall()

    return {
        "id": [r[0] for r in result],
        "agent-name": [r[1] for r in result],
        "hostname": [r[2] for r in result],
        "ip": [r[3] for r in result],
        "os": [r[4] for r in result],
        "status": [r[5] for r in result],
        "group_id": [r[6] for r in result]
    }
def getAgentsInGroup(group_id):
    query = 'select * from agents where group_id = ?'
    cursor.execute(query, (group_id,))
    result = cursor.fetchall()

    return {
        "id": [r[0] for r in result],
        "agent-name": [r[1] for r in result],
        "hostname": [r[2] for r in result],
        "ip": [r[3] for r in result],
        "os": [r[4] for r in result],
        "status": [r[5] for r in result],
        "group_id": [r[6] for r in result]
    }
def getAgentIdFromIp(ip):
    query = 'select agent_id from agents where host_ip = ?'
    cursor.execute(query, (ip, ))
    result = cursor.fetchall()
    return {
        'id': [r[0] for r in result]
    }

def getSysinfo(id):
    query = 'select * from sysinfo where agent_id = ?'
    cursor.execute(query, (id,))
    result = cursor.fetchall()
    return {
        "id": [r[0] for r in result],
        "timestamp_2": [r[1] for r in result],
        "cpu": [r[2] for r in result],
        "ram": [r[3] for r in result],
        "disk_": [r[4] for r in result]
    }

def deleteAgent(id):
    query_2 = 'update agents set group_id = NULL where agent_id = ?'
    cursor.execute(query_2, (id, ))
    conn.commit()

def deleteGroup(group_id):
    query_1 = 'update agents set group_id = NULL where group_id = ?'
    query_2 = 'delete from group_host where group_id = ?'
    cursor.execute(query_1, (group_id, ))
    conn.commit()
    cursor.execute(query_2, (group_id, ))
    conn.commit()
