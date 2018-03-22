import sys, time
from wifi_client_list import *

if __name__ == '__main__':
    print('Retrieving connected devices ..')

    devices = parse_arp()
    
    if not devices:
        print('No devices found!')
        sys.exit(-1)
    print("Devices found")
    for device in devices:
        ip = device[0]
        mac = device[1]
        
        device_verify_url = "http://%s/id?"%(ip)
        print(device_verify_url)
        try:
            id = requests.get(device_verify_url).text
            print(id)
        except Exception as e:
            print(e)
            id = None
        if id: #valid solar data collection device
            timestamp = time.strftime("%d%H%m")
            data_retrieve_url = "http://%s/solarData.txt?%s"%(ip, timestamp)
            data = requests.get(data_retrieve_url).text
            f = open("solar_data/%s_%s.txt"%(ip,timestamp),"w")
            f.write(data)
            f.close()
