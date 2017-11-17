import serial
from utils import log
from .Config import SERIAL_HEAD,SERIAL_TAIL,PORT_NAME,BAUDRATE,MACHINE_A,MACHINE_B,OTHER_SPEED
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
        log.log('串口发送'+data)
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

    def __vertical(self, machine, angle):
        log.log('设定俯仰角度：'+machine+str(angle))
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

        data = '0301' + hundreds + tens + ones + dot1
        target = MACHINE_A
        if machine == 'machineB' or machine == 'B' or machine == 'b':
            target = MACHINE_B
        self.__send_data(data_length='06',
                         data_code=data,
                         target_address=target
                         )
        time.sleep(1)

    def __horizontal(self, machine, angle):
        log.log('设定水平角度：'+machine + str(angle))
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
        target = MACHINE_A
        if machine == 'machineB' or machine == 'B' or machine == 'b':
            target = MACHINE_B
        self.__send_data(data_length='06',
                         data_code=data,
                         target_address=target
                         )
        time.sleep(1)

    def __upspeed(self, machine, speed):
        hundreds = int(speed / 1000)
        tens = int((speed - hundreds * 1000) / 100)
        ones = int((speed - hundreds * 1000 - tens * 100) / 10)
        dot1 = int((speed - hundreds * 1000 - tens * 100 - ones * 10) * 1)

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

        data = '0305' + hundreds + tens + ones + dot1
        if machine == 'machineB' or machine == 'B' or machine == 'b':
            target = MACHINE_B
        else:
            target = MACHINE_A
        self.__send_data(data_length='06',
                         data_code=data,
                         target_address=target
                         )

    def __downspeed(self, machine, speed):
        hundreds = int(speed / 1000)
        tens = int((speed - hundreds * 1000) / 100)
        ones = int((speed - hundreds * 1000 - tens * 100) / 10)
        dot1 = int((speed - hundreds * 1000 - tens * 100 - ones * 10) * 1)

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

        data = '0307' + hundreds + tens + ones + dot1
        if machine == 'machineB' or 'B' or 'b':
            target = MACHINE_B
        else:
            target = MACHINE_A
        self.__send_data(data_length='06',
                         data_code=data,
                         target_address=target
                         )

    def shoot(self, machine, point, director):
        log.log('发球机器' + str(machine) + '-点' + str(point) + '-回球指导' + str(director))
        # 设定回球指导
        self.guide(1, False)
        self.guide(2, False)
        self.guide(director, True)
        point = 'point'+str(point)
        if machine == 'machineA' or 'A':
            # TODO machineA 参数设定
            point_args = self.args['machineA'][point]
            upspeed = point_args['upspeed']
            downspeed = point_args['downspeed']
            vertical = point_args['vertical']
            horizontal = point_args['horizontal']
            # 设定角度转速
            self.__horizontal('A', horizontal)
            self.__vertical('A', vertical)
            upspeed = str(hex(upspeed))[2:].capitalize()
            downspeed = str(hex(downspeed))[2:].capitalize()
            speed = str(hex(OTHER_SPEED))[2:].capitalize()
            self.__send_data(data_length='06',
                             data_code='0202'+upspeed+downspeed+speed+'00',
                             target_address=MACHINE_A)
            pass
        elif machine == 'machineB' or 'B':
            # TODO machineB 参数设定
            point_args = self.args['machineB'][point]
            upspeed = point_args['upspeed']
            downspeed = point_args['downspeed']
            vertical = point_args['vertical']
            horizontal = point_args['horizontal']
            self.__horizontal('B', horizontal)
            self.__vertical('B', vertical)
            upspeed = str(hex(upspeed))[2:].capitalize()
            downspeed = str(hex(downspeed))[2:].capitalize()
            speed = str(hex(OTHER_SPEED))[2:].capitalize()
            self.__send_data(data_length='06',
                             data_code='0202'+upspeed+downspeed+speed+'00',
                             target_address=MACHINE_B)
            pass
        pass

    def start(self):
        log.log('启动网球机')
        self.__send_data('06', '01015A5A0000')
        time.sleep(1)
        self.__send_data('06', '01015A5A0000', target_address=MACHINE_B)

    def stop(self):
        log.log('停止网球机运行')
        self.__send_data('02', '0102')
        time.sleep(1)
        self.__send_data('02', '0102', target_address=MACHINE_B)

    def guide(self, number, status):
        if number == 1:
            if status is True:
                self.__send_data('02','0501',target_address='01')
            else:
                self.__send_data('02', '0502', target_address='01')
        elif number == 2:
            if status is True:
                self.__send_data('02','0501',target_address='02')
            else:
                self.__send_data('02', '0502', target_address='02')
        elif number == 3:
            if status is True:
                self.__send_data('02','0501',target_address='03')
            else:
                self.__send_data('02', '0502', target_address='03')
        elif number == 4:
            if status is True:
                self.__send_data('02','0501',target_address='04')
            else:
                self.__send_data('02', '0502', target_address='04')

    def vertical(self, angle):
        self.__vertical('A', angle)
