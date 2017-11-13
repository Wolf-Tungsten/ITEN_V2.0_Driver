import serial
from utils import log
from .Config import SERIAL_HEAD,SERIAL_TAIL,PORT_NAME,BAUDRATE
import binascii
import time

class Device(object):
    def __init__(self, com):
        self.com = com
        self.args = {}

    def __send_data(self, data_length, data_code, source_address='E1', target_address='53'):
        # 奇偶校验
        def __parity_check(data):
            binary = binascii.a2b_hex(data)
            check = binary[2]
            for i in binary[3:]:
                check = check ^ i
            check = hex(check)[2:].capitalize()
            if len(check) < 2:
                check = '0' + check
            data = data + check + SERIAL_TAIL
            return data
        data = SERIAL_HEAD + source_address + target_address + data_length + data_code
        data = __parity_check(data)
        print(data)
        try:
            self.port = serial.Serial(PORT_NAME, BAUDRATE)
            try:
                for counter in range(1):
                    for i in range(0,int(len(data)/2)):
                        byte = data[i*2:i*2+2]
                        byte = binascii.a2b_hex(byte)
                        time.sleep(0.05)
                        self.port.write(byte)
            except Exception as e:
                print(e)
            finally:
                self.port.close()
        except Exception as e:
            print(e)

    def __vertical(self, angle):
        hundreds = int(angle / 1000)
        tens = int((angle - hundreds * 1000) / 100)
        ones = int((angle - hundreds * 1000 - tens * 100) / 10)
        dot1 = int((angle - hundreds * 1000 - tens * 100 - ones * 10) * 1)

        hundreds = str(hex(hundreds))[2:].capitalize()
        tens = str(hex(tens))[2:].capitalize()
        ones = str(hex(ones))[2:].capitalize()
        dot1 = str(hex(dot1))[2:].capitalize()

        if len(hundreds) < 2:
            hundreds = '0' + hundreds
        if len(tens) < 2:
            tens = '0' + tens
        if len(ones) < 2:
            ones = '0' + ones
        if len(dot1) < 2:
            dot1 = '0' + dot1

        data = '0303' + hundreds + tens + ones + dot1
        self.__send_data(data_length='06',
                         data_code=data
                         )
        pass

    def __horizontal(self, angle):
        pass

    def shoot(self, machine, point, director):
        # TODO 发球指令
        log.log('发球')
        pass

    def start(self):
        log.log('启动网球机')
        self.__send_data('06', '01015A5A0000')

    def stop(self):
        # TODO 网球机终止指令
        log.log('停止网球机运行')
        self.__send_data('02', '0102')

    def guide(self, number, status):
        if number == 1:
            if status is True:
                self.__send_data('02','0501',target_address='01')
            else:
                self.__send_data('02', '0502', target_address='01')
        else:
            if status is True:
                self.__send_data('02','0501',target_address='02')
            else:
                self.__send_data('02', '0502', target_address='02')