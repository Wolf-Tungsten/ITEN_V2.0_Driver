import requests
import json
import getpass

print("""
  _____ _______ ______ _   _  __      _____    ___  
 |_   _|__   __|  ____| \ | | \ \    / /__ \  / _ \ 
   | |    | |  | |__  |  \| |  \ \  / /   ) || | | |
   | |    | |  |  __| | . ` |   \ \/ /   / / | | | |
  _| |_   | |  | |____| |\  |    \  /   / /_ | |_| |
 |_____|  |_|  |______|_| \_|     \/   |____(_)___/ 

""")
print("ITEN-网球机训练模式设置工具")
server = input("服务器地址:(https://wolf.myseu.cn/itenserv)")
if server == '':
    server = 'https://wolf.myseu.cn/itenserv'
username = input("请输入管理员用户名:")
password = getpass.getpass('请输入管理员用户密码:')
print('正在检查权限是否合法...')
res = requests.post(server + '/auth/signin', data={'username': username, 'password': password})
res = res.json()
if 'flag' in res and res['flag'] is True:
    token = res['token']
    print('登录成功！')
else:
    input('登录失败！按回车键退出')
    exit()
header = {
    'Access-Token': token
}
while True:
    res = requests.get(server+'/trainmode/available')
    res = res.json()
    current = {}
    print('当前可用模式：')
    for mode in res['available_list']:
        current[mode['train_name']] = mode['_id']
        print('* '+mode['train_name']+' id:'+mode['_id'])
    operator = input('请输入操作代号|a-添加|d-删除：')
    if operator == 'd':
        while True:
            train_name = input('要删除的训练名称：')
            if train_name in current:
                data = {'train_id':current[train_name]}
                requests.delete(server+'/trainmode/delete', headers=header, data=data)
                break
            else:
                print('训练名称不存在，请重试')
    if operator == 'a':
        template = {
            'type':'cycle',
            'cycle':[]
        }
        name = input('训练模式名称:')
        if name in current:
            print('已存在的名称！请重试')
        else:
            while True:
                flag = input('按回车添加一个点（输入s停止）')
                if flag == 'n':
                    break
                machine = input('使用发球机（a|b）：')
                if machine == 'a':
                    machine = 'machineA'
                elif machine == 'b':
                    machine = 'machineB'
                else:
                    print('输入有误请重试')
                    continue
                point = int(input('请输入击球点（1-16）：'))
                if not 1 <= point <= 16:
                    print('输入有误请重试')
                    continue
                director = int(input('请输入回球指导（1-4）：'))
                if not 1 <= director <= 4:
                    print('输入有误请重试')
                    continue
                new = {
                    'machine': machine,
                    'point': point,
                    'director': director
                }
                template['cycle'].append(new)
            data = {'train_name':name,
                    'train_data':json.dumps(template)}
            requests.post(server + '/trainmode/add', headers=header, data=data)


