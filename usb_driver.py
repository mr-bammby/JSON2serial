import serial
import os.path
import datetime
import time

class USB_conn:
    write_mask = int("00000101", 2)
    read_mask =  int("00000100", 2)
    cs_mask =    int("00000010", 2)
    message_mask = int("11111111", 2)
    def __init__(self, com, baudrate, timeout, logging = True, log_name = "./log/log"):
        self.ser = serial.Serial(com, baudrate, timeout=timeout)
        self.logging = logging
        if self.logging:
            self.log_name = log_name
            counter = 0
            while (os.path.isfile(self.log_name)):
                self.log_name = log_name + str(counter)
                counter = counter + 1
            self.file = open(self.log_name, 'a')

    def read(self, message, cs, read_message = 0):
        if cs not in [1, 2]:
            print ("Un known cs")
            return
        if message != None:
            self.write(message, cs)
        mask = self.read_mask
        if cs == 2:
            mask = mask | self.cs_mask
        time.sleep(0.01)
        self.ser.write(bytes([mask]))
        time.sleep(0.01)
        self.ser.write(bytes([read_message]))
        if self.logging:
            ct = datetime.datetime.now()
            self.file.write(str(ct))
            self.file.write("  write  ")
            self.file.write(hex(mask))
            self.file.write("\\")
            self.file.write(hex(read_message))
            self.file.write("\n")
        command = self.ser.read()
        message = self.ser.read()
        if self.logging:
            ct = datetime.datetime.now()
            self.file.write(str(ct))
            self.file.write("  read   ")
            self.file.write("0x")
            self.file.write(str(command.hex()))
            self.file.write("\\")
            self.file.write("0x")
            self.file.write(str(message.hex()))
            self.file.write("\n")

    def write(self, message, cs):
        if cs not in [1, 2]:
            print ("Un known cs")
            return
        write_message = message
        mask = self.write_mask
        if cs == 2:
            mask = mask | self.cs_mask
        time.sleep(0.01)
        self.ser.write(bytes([mask]))
        time.sleep(0.01)
        self.ser.write(bytes([write_message]))
        if self.logging:
            ct = datetime.datetime.now()
            self.file.write(str(ct))
            self.file.write("  write  ")
            self.file.write(hex(mask))
            self.file.write("\\")
            self.file.write(hex(write_message))
            self.file.write("\n")

    def close(self):
        self.file.close()
        self.ser.close()