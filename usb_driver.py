import serial
import os.path
import datetime
import time

def byte_counter(message):
    bit_len = len(bin(message)) - 2
    byte_len = bit_len / 8;
    if (bit_len % 8) != 0:
        byte_len = byte_len + 1;
    return byte_len

class USB_conn:
    write_mask = int("00000001", 2)
    read_mask =  int("00000000", 2)
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

    def int_to_bytes(self, message):
        byte_num = byte_counter(message);
        byte_list = []
        for _ in range(byte_num):
            byte_list.append(message & self.message_mask)
            message = message>>8;

    def read(self, message, cs, read_message = 0):
        if cs not in [1, 2]:
            print ("Un known cs")
            return
        if message != "None":
            self.write(message, cs)
        mask = self.read_mask
        if cs == 2:
            mask = mask | self.cs_mask
        message_list = self.int_to_bytes(read_message) #max number of btes in message is 2^6
        message_len = len(message_list)
        mask = mask & (message_len<<2)
        self.ser.write(bytes([mask]))
        if self.logging:
            ct = datetime.datetime.now()
            self.file.write(str(ct))
            self.file.write("  write  ")
            self.file.write(hex(mask))
        for i in range(message_len):
            	self.ser.write(bytes([message_list[i]]))
            if self.logging:
                self.file.write("\\")
                self.file.write(hex(message_list[i]))
        if self.logging:
            self.file.write("\n")
        command = self.ser.read()
        message_len = command>>2
        if self.logging:
            ct = datetime.datetime.now()
            self.file.write(str(ct))
            self.file.write("  read   ")
            self.file.write("0x")
            self.file.write(str(command.hex()))
        else:
            print(str(ct) + " read  ")
            print("0x" + str(command.hex()))
        for _ in range(message_len):
            message = self.ser.read()
            if self.logging:
                self.file.write("\\")
                self.file.write("0x")
                self.file.write(str(message.hex()))
            else:
                print("\\0x" + str(message.hex()))
        if self.logging:
            self.file.write("\n")
            
    def write(self, message, cs):
        if cs not in [1, 2]:
            print ("Un known cs")
            return
        write_message = message
        mask = self.write_mask
        if cs == 2:
            mask = mask | self.cs_mask
        message_list = self.int_to_bytes(read_message) #max number of btes in message is 2^6
        message_len = len(message_list)
        mask = mask & (message_len<<2)
        self.ser.write(bytes([mask]))
        if self.logging:
            ct = datetime.datetime.now()
            self.file.write(str(ct))
            self.file.write("  write  ")
            self.file.write(hex(mask))
        for i in range(message_len):
            	self.ser.write(bytes([message_list[i]]))
            if self.logging:
                self.file.write("\\")
                self.file.write(hex(message_list[i]))
        if self.logging:
            self.file.write("\n")

    def close(self):
        self.file.close()
        self.ser.close()