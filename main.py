import json
import time
import usb_driver

def toUSB(line):
    if line['action'] == "write":
        USBconn.write(line['message'], line['cs'])
    elif line['action'] == "read":
        if 'read_message' in line:
            USBconn.read(line['message'], line['cs'], read_message=line['read_message'])
        else:
            USBconn.read(line['message'], line['cs'])

file_json = open("exsettings.json")
data = json.load(file_json)
setup = data['setup']
if 'log_file' in setup.keys():
    USBconn = usb_driver.USB_conn(setup['com'], setup['baudrate'], setup['timeout'], log_name=setup['log_file'])
else:
    USBconn = usb_driver.USB_conn(setup['com'], setup['baudrate'], setup['timeout'])

USBconn.write(0, 1)
USBconn.write(0, 2)
while (1):
    if setup['type'] == "relative":
        for line in data['timeline']:
            time.sleep(line['delay_ms'] / 1000.0)
            toUSB(line)
    if setup['type'] == "absolute":
        start_time_ns = time.time_ns()
        for line in data['timeline']:
            while True:
                time_ns = time.time_ns()
                if ((time_ns - start_time_ns) / 1000000.0) > line['delay_ms']:
                    break
                time.sleep(5/10000)
            toUSB(line)
    if setup['loop'] == "single":
        break
USBconn.close()