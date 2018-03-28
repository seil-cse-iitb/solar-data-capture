from flask import Flask, render_template, send_from_directory, Response
import sys, time, json, urllib.request, socket
from wifi_client_list import *
timeout=10
socket.setdefaulttimeout(timeout)


app = Flask(__name__)

@app.route("/")
def index():
	return render_template('index.html')

@app.route("/client")
def client_index():
	print('Retrieving connected clients ..')

	clients = parse_arp()

	if not clients:
		print('No clients found!')
		sys.exit(-1)

	devices=[]
	for client in clients:
		ip = client[0]
		mac = client[1]
		try:
			with urllib.request.urlopen('http://%s/id?'%(ip)) as response:
				id = response.read().decode()
		except Exception as e:
			print(e)
			continue
		devices.append({"id":id,"ip":ip,"mac":mac})

	return Response(json.dumps(devices),  mimetype='application/json')

@app.route('/js/<path:path>')
def send_js(path):
	return send_from_directory('templates/js', path)

@app.route('/node_modules/<path:path>')
def send_node_modules(path):
	return send_from_directory('templates/node_modules', path)

@app.route('/css/<path:path>')
def send_css(path):
	return send_from_directory('templates/css', path)
	
@app.route('/fonts/<path:path>')
def send_fonts(path):
	return send_from_directory('templates/fonts', path)

if __name__ == "__main__":
    app.run(host="0.0.0.0")
