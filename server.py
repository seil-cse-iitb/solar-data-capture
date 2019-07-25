from flask import Flask, render_template, send_from_directory, Response
import sys
import time
import json
import urllib.request
import socket
import os
import shutil
import threading
from datetime import datetime
from wifi_client_list import *
timeout = 10
socket.setdefaulttimeout(timeout)

devices = {}
live_data_threads = {}
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
            with urllib.request.urlopen('http://%s/id?' % (ip)) as response:
                id = response.read().decode()
        except Exception as e:
            print(e)
            continue
        # devices.append({"id":id,"ip":ip,"mac":mac})
        devices[ip] = {"id": id, "mac": mac, "ip": ip}
        download(ip, datetime.now().strftime('%d%H%M'), browser_initiated)
    if browser_initiated:
        return Response(json.dumps(devices),  mimetype='application/json')


@app.route('/download/<path:ip>/<path:timestamp>')
def download(ip, timestamp, browser_initiated=True):
    data_retrieve_url = "http://%s/solarData.txt?%s" % (ip, timestamp)
    data = requests.get(data_retrieve_url).text
    f = open(os.path.join(app.root_path, "solar_data/%s_%s.txt" %
                          (devices[ip]["id"], timestamp)), "w")
    f.write(data)
    f.close()
    if browser_initiated:
        return send_from_directory('solar_data', os.path.basename(f.name))


class LiveDataThread(threading.Thread):
    # Thread class with a _stop() method.
    # The thread itself has to check
    # regularly for the stopped condition.

    def __init__(self, *args, **kwargs):
        self.ip = args[0]
        self.timestamp = args[1]
        # super(LiveDataThread, self).__init__(*args, **kwargs)
        self.stopped = False
        threading.Thread.__init__(self)

    # function using _stop function
    def stop(self):
        self.stopped = True

    def run(self):
        data_retrieve_url = "http://%s/liveData" % (self.ip)
        local_filename = os.path.join(
            app.root_path, "solar_data/%s_%s_live.txt" % (self.ip, self.timestamp))
        r = requests.get(data_retrieve_url, stream=True)
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024):
                if self.stopped:
                    break            
                if chunk:  # filter out keep-alive new chunks
                    f.write(chunk)
        r.close()
        return


@app.route('/start_live_data/<path:ip>/<path:timestamp>')
def start_live_data(ip, timestamp):
    t1 = LiveDataThread(ip, timestamp)
    t1.start()
    live_data_threads[t1.getName()] = t1
    return t1.getName()

@app.route('/stop_live_data/<path:thread_name>')
def stop_live_data(thread_name):
    t1 = live_data_threads[thread_name]
    t1.stop()
    t1.join()
    filename = "%s_%s_live.txt" % (t1.ip, t1.timestamp)
    del live_data_threads[thread_name]
    return send_from_directory('solar_data', os.path.basename(filename))

@app.route('/debug/<path:ip>/<path:message>')
def debug(ip, message):
    debug_send_url = "http://%s/debug?%s" % (ip, message)
    try:
        with urllib.request.urlopen(debug_send_url) as response:
            response = response.read().decode()
        # return Response({"message":"Debug sent"},  mimetype='application/json')
    except Exception as e:
        print(e)
    return Response(json.dumps({"message": "Debug sent"}),  mimetype='application/json')


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
