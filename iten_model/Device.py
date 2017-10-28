import serial


class Device(object):
    def __init__(self, com):
        self.com = com
        self.args = {}

    def shoot(self, machine, point, director):
        # TODO 发球指令
        pass
    def start(self):
        # TODO 网球机启动指令
        pass
    def stop(self):
        # TODO 网球机终止指令
        pass
