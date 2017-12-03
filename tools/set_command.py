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
print("ITEN-网球机命令工具")
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
    machine_id = input('请输入网球机id:')
    data = {}
    data['machine_id'] = machine_id
    print('* 启用视觉 - enable_cv')
    print('* 停用视觉 - disable_cv')
    command = input('请输入命令')
    data['command'] = command
    requests.post(server+'/hardware/command', headers=header, data=data)











