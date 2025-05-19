from flask import Flask, render_template, jsonify, request, url_for, redirect
from config import db
from controller import home
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

conn = db.connect()
cursor = conn.cursor()

@app.route('/')
def dashboard():  # put application's code here
    return redirect(url_for('group'))

@app.route('/groups')
def group():
    data = []
    raw_data = home.getGroupHost()
    len_raw = len(raw_data.get('id'))
    for i in range(0, len_raw):
        item = []
        for j in raw_data:
            item.append(raw_data.get(j)[i])
        data.append(item)
    return render_template('group.html', groups=data)

@app.route('/agents')
def agents():
    data = []
    raw_data = home.getAgents()
    for i in range(0, len(raw_data.get('id'))):
        items = []
        for k, v in raw_data.items():
            items.append(raw_data.get(k)[i])
        data.append(items)
    return render_template("agents.html", agents=data)

@app.route('/api/agent-report', methods=['POST'])
def receive_agent_data():
    data = request.get_json()
    home.addAgent(data)
    return jsonify({"status": "success"}), 200

@app.route('/create_group', methods=['POST', 'GET'])
def create_group():
    if request.method == 'POST':
        name = request.form.get("groupname")
        location = request.form.get('location')
        home.addGroupHost(name, location)
        return redirect(url_for('group'))  # nếu GET thì hiển thị form
    return render_template("create_group.html")

@app.route('/groups/addagent/<int:group_id>', methods=['GET', 'POST'])
def addAgent(group_id):
    data = []
    raw_data = home.getAgents()
    for i in range(0, len(raw_data.get('id'))):
        items = []
        for k, v in raw_data.items():
            items.append(raw_data.get(k)[i])
        if items[6] is not None:
            items.append(1)
        else:
            items.append(0)
        data.append(items)
    agent_of_id = [i for i in data if i[6] == group_id]
    return render_template('addAgent.html', agents=data, id=group_id, agent_of_id=agent_of_id)

@app.route('/groups/addagent/delete/<int:group_id>/<int:agent_id>', methods=['GET', 'POST'])
def deleteAgent(group_id, agent_id):
    home.deleteAgent(agent_id)
    return redirect(url_for('addAgent', group_id=group_id))

@app.route('/groups/<int:group_id>/<int:agent_id>', methods=['POST', 'GET'])
def addAgentIntoGroup(group_id, agent_id):
    home.addAgentIntoGroup(group_id, agent_id)
    return redirect(url_for('addAgent', group_id=group_id))

@app.route('/groups/<int:group_id>', methods=['POST', 'GET'])
def deleteGroup(group_id):
    home.deleteGroup(group_id)
    return redirect(url_for('group'))

@app.route('/chart/<int:id>')
def chart(id):
    return render_template('chart.html', id=id)

@app.route('/api/chart-data/<int:agent_id>', methods=['GET'])
def get_chart_data(agent_id):
    network = home.getNetTraffic(agent_id)
    sysinfo = home.getSysinfo(agent_id)
    data = network | sysinfo
    return jsonify(data)

@app.route('/api/addagent', methods=['POST'])
def getInfo():
    data = request.get_json()
    home.addAgent(data)
    return jsonify({"status": "success"}), 200

@app.route('/api/sysinfo', methods=['POST', 'GET'])
def sendsysinfo():
    data = request.get_json()
    ip = data['ip']
    id = home.getAgentIdFromIp(ip)
    home.addSysInfo(data, id['id'][0])
    return jsonify({"status": "success"}), 200

@app.route('/api/network', methods=['POST'])
def netinfo():
    data = request.get_json()
    ip = data['ip']
    id = home.getAgentIdFromIp(ip)
    print(id)
    home.addNetTraffic(data, id['id'][0])
    return jsonify({"status":"success"}), 200

@app.route('/api/getsysinfo', methods=['POST'])
def net_monitor():
    data = request.get_json()
    ip = data['ip']
    id = home.getAgentIdFromIp(ip)
    home.addNetTraffic(data, id['id'][0])
    return jsonify({"status":"success"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)