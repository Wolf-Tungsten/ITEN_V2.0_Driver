import requests
import json
import threading
import time
from iten_model.Device import Device
from iten_model.Vision import Vision
from utils import log


class Machine(object):
    def __init__(self, machine_id, com, server, camera):
        self.machine_id = machine_id
        self.state = {
            'machine_id': machine_id,
            'state': 'free',
            'train_id': '',
            'train_name': '',
            'train_amount': 0,
            'train_count': 0,
            'user_id': ''
        }
        self.train_data = {}
        self.server = server
        self.device = Device(com)
        self.vision = Vision(camera)
        self.get_args()
        self.active_thread = threading.Thread(target=self.active, name="Active Thread")
        self.active_thread.run()

    def get_request(self, route, params=None):
        res = requests.get(self.server+route, params=params)
        res.encoding = 'utf8'
        return res.json()

    def post_request(self, route, data=None):
        res = requests.post(self.server+route, data=data)
        res.encoding = 'utf8'
        return res.json()

    def get_args(self):
        res = self.get_request('/hardware/arguments', params={'machine_id': self.machine_id})
        if res['has']:
            args = res['arguments']
            args = json.loads(args)
            self.device.args = args
            log.log('参数设置获取成功')
        else:
            print('未获取到参数，启动失败')
            exit(-1)

    def active(self):
        log.log('网络通讯线程开始运行')
        while True:
            time.sleep(5)
            data = self.state
            server_state = self.post_request('/hardware/active', data=data)
            if self.state['state'] == 'free':
                if server_state['state'] == 'deploying':
                    self.state['state'] = 'working'
                    self.state['train_id'] = server_state['train_id']
                    self.get_train_data(server_state['train_id'])
                    self.state['train_amount'] = server_state['train_amount']
                    self.state['train_count'] = 0
                    self.state['user_id'] = server_state['user_id']
                    log.log('用户：%s-部署任务'%server_state['user_id'])
            elif self.state['state'] == 'working':
                if server_state['state'] == 'pause' or 'free':
                    self.state['state'] = server_state['state']
            elif self.state['state'] == 'pause':
                if server_state['state'] == 'working':
                    self.state['state'] = 'working'
                elif server_state['state'] == 'free':
                    self.state['state'] = 'free'
            log.log('向服务器更新状态')

    def get_train_data(self, train_id):
        res = self.get_request('/trainmode/data', params={'train_id': train_id})
        self.train_data = json.loads(res['train_data'])
        self.state['train_name'] = res['train_name']
        log.log('训练模式被设置为：%s' % self.state['train_name'])





