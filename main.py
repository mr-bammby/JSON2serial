import json
import time

def toUSB(line):
	if line['action'] == "write":
		USBconn.write(line['message'])
	elif line['action'] == "read":
		USBconn.read(line['message'])

file_json = open("setting.json")
data = json.load(file_json)

if data['type'] == "relative":
    for line in data['timeline']:
		toUSB(line)
        time.sleep(line['delay_ms'] / 1000)
if data['type'] == "absolute":
    start_time_ms = time.time_ns() / 1000
    for line in data['timeline']:
        toUSB(line)
        time_ms = time.time_ns() / 1000
        while True:
            if (time_ms - start_time_ms) > line['delay_ms']:
                break
            time.sleep(5/10000)