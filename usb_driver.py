import serial
import os.path
import datetime

class USB_conn:
    write_mask = int("10100000000", 2)
    read_mask =  int("10000000000", 2)
    cs_mask =    int("01000000000", 2)
    message_mask = int("11111111", 2)
    def __init__(self, com, baudrate, timeout, logging = True, log_name = ".\log\log"):
        self.ser = serial.Serial(com, baudrate, timeout=timeout)
        self.logging = logging
        if self.logging:
            self.log_name = log_name
            counter = 0
            while (os.path.isfile(self.log_name)):
                self.log_name = log_name + str(counter)
                counter = counter + 1
            self.file = open(self.log_name, 'a')

    def read(self, message, cs, buff):
        self.write(message, cs)
        read_message = 0
        mask = self.read_mask
        if cs == 2:
            mask = mask | self.cs_mask
        self.ser.write(bytes([read_message]))
        self.ser.write(bytes([mask >> 8]))
        if self.logging:
            ct = datetime.datetime.now()
            self.file.write(str(ct))
            self.file.write("  write  ")
            self.file.write(int(read_message).to_bytes(2, byteorder='big').hex("\\"))
            self.file.write("\n")
        message = self.ser.read()
        command = self.ser.read()
        if self.logging:
            ct = datetime.datetime.now()
            self.file.write(str(ct))
            self.file.write("  read   ")
            self.file.write(str(command.hex()))
            self.file.write("\\")
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
        self.ser.write(bytes([write_message]))
        self.ser.write(bytes([mask >> 8]))
        if self.logging:
            ct = datetime.datetime.now()
            self.file.write(str(ct))
            self.file.write("  write  ")
            self.file.write(int(write_message).to_bytes(2, byteorder='big').hex("\\"))
            self.file.write("\n")

    def close(self):
        self.file.close()
        self.ser.close()