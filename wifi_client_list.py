import subprocess
import re
import requests

# Store Mac address of all nodes here
saved = {
    'xx:xx:xx:xx:xx:xx': 'My laptop',
}

# Set wireless interface using ifconfig
interface = "wlan0"

mac_regex = re.compile(r'([a-zA-Z0-9]{2}:){5}[a-zA-Z0-9]{2}')


def parse_arp():
    arp_out = subprocess.check_output('arp -e -i %s'%(interface), shell=True).decode('utf-8')
    print(arp_out)
    if 'no match found' in arp_out:
        return None

    result = []
    for lines in arp_out.strip().split('\n'):
        line = lines.split()
        if interface in line and '(incomplete)' not in line:
            for element in line:
                # If its a mac addr
                if mac_regex.match(element):
                    result.append((line[0], element))
    return result


def get_mac_vendor(devices):
    num = 0
    for device in devices:
        try:
            url = "http://api.macvendors.com/%s"%(device[1])
            try:
                vendor = requests.get(url).text
            except Exception as e:
                print(e)
                vendor = None

        except Exception as e:
            print("Error occured while getting mac vendor", e)

        num += 1
        print_device(device, num, vendor)

def print_device(device, num=0, vendor=None):
    device_name = saved[device[1]] if device[1] in saved else 'unrecognised !!'

    print('\n%s'%(device_name),  '\nVendor:', vendor, '\nMac:', device[1], '\nIP: ',device[0])

if __name__ == '__main__':
    print('Retrieving connected devices ..')

    devices = parse_arp()

    if not devices:
        print('No devices found!')

    else:
        print('Retrieving mac vendors ..')
        try:
            get_mac_vendor(devices)

        except KeyboardInterrupt as e:
            num = 0
            for device in devices:
                num += 1
                print_device(device, num)
