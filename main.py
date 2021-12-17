import json
import time
import usb_driver

def toUSB(line):
    if line['action'] == "write":
        USBconn.write(line['message'])
    elif line['action'] == "read":
        USBconn.read(line['message'])


file_json = open("exsetting.json")
data = json.load(file_json)
setup = data['setup']
if 'log_file' in setup.keys():
    USBconn = usb_driver.USB_conn("COM3", 9600, setup['timeout'])
else:
    USBconn = usb_driver.USB_conn("COM3", 9600, setup['timeout'], log_name=setup['log_file'])
if setup['type'] == "relative":
    for line in data['timeline']:
        toUSB(line)
        time.sleep(line['delay_ms'] / 1000)
if setup['type'] == "absolute":
    start_time_ms = time.time_ns() / 1000
    for line in data['timeline']:
        toUSB(line)
        time_ms = time.time_ns() / 1000
        while True:
            if (time_ms - start_time_ms) > line['delay_ms']:
                break
            time.sleep(5/10000)
