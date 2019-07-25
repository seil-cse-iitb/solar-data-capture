from flask import Flask, render_template, send_from_directory, Response
import sys, time, json, urllib.request, socket, os, shutil
from datetime import datetime
from wifi_client_list import *
timeout=10
socket.setdefaulttimeout(timeout)

devices={}
app = Flask(__name__)

@app.route("/")
def index():
	return render_template('index.html')

@app.route("/client")
def client_index(browser_initiated=True):
	print('Retrieving connected clients ..')

	clients = parse_arp()

	if not clients:
		print('No clients found!')
		sys.exit(-1)

	# devices=[]
	for client in clients:
		ip = client[0]
		mac = client[1]
		try:
			with urllib.request.urlopen('http://%s/id?'%(ip)) as response:
				id = response.read().decode()
		except Exception as e:
			print(e)
			continue
		# devices.append({"id":id,"ip":ip,"mac":mac})
		devices[ip] = {"id":id, "mac":mac, "ip":ip}
		download(ip, datetime.now().strftime('%d%H%M'), browser_initiated)
	if browser_initiated:
		return Response(json.dumps(devices),  mimetype='application/json')

@app.route('/download/<path:ip>/<path:timestamp>')
def download(ip,timestamp, browser_initiated=True):
	data_retrieve_url = "http://%s/solarData.txt?%s"%(ip, timestamp)
	data = requests.get(data_retrieve_url).text
	f = open(os.path.join(app.root_path,"solar_data/%s_%s.txt"%(devices[ip]["id"],timestamp)),"w")
	f.write(data)
	f.close()
	if browser_initiated:
		return send_from_directory('solar_data',os.path.basename(f.name))

@app.route('/live_data/<path:ip>/<path:timestamp>')
def live_data(ip, timestamp):
	data_retrieve_url = "http://%s/liveData"%(ip)
	local_filename = os.path.join(app.root_path,"solar_data/%s_%s_live.txt"%(ip,timestamp))
	r = requests.get(data_retrieve_url, stream = True)
	with open(local_filename, 'wb') as f:
		for chunk in r.iter_content(chunk_size=1024): 
			if chunk: # filter out keep-alive new chunks
				f.write(chunk)
				#f.flush() commented by recommendation from J.F.Sebastian
	r.close()
#	return local_filename
#	with requests.get(data_retrieve_url, stream=True) as r:
#		with open (local_filename, 'wb') as f:
#			shutil.copyfileobj(r.raw, f)
	print ("Streaming ended")
	return local_filename

@app.route('/debug/<path:ip>/<path:message>')
def debug(ip, message):
	debug_send_url = "http://%s/debug?%s"%(ip, message)
	try:
		with urllib.request.urlopen(debug_send_url) as response:
			response = response.read().decode()
		# return Response({"message":"Debug sent"},  mimetype='application/json')
	except Exception as e:
		print(e)
	return Response(json.dumps({"message":"Debug sent"}),  mimetype='application/json')


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
    print("Performing initial scan and download.")
    client_index(browser_initiated=False)
    print("Starting server")
    app.run(host="0.0.0.0")
