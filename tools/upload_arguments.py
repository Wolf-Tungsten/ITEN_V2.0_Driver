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
print("ITEN-网球机参数设定工具")
print("请按照提示进行操作")
server = input("服务器地址:(http://wolf.myseu.cn:5197/itenserv)")
if server == '':
    server = 'http://wolf.myseu.cn:5197/itenserv'
username = input("请输入管理员用户名:")
password = getpass.getpass('请输入管理员用户密码:')
print('正在检查权限是否合法...')
res = requests.post(server+'/auth/signin', data={'username': username, 'password': password})
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
machine_id = input('请输入网球机id:')
print('正在检查是否已经存在参数...')
res = requests.get(server+'/hardware/arguments', params={'machine_id': machine_id})
has = res.json()['has']
if has:
    print('网球机%s已有参数设置，将进入修改模式' % machine_id)
    args = json.loads(res.json()['arguments'])
    for machine in args:
        print('<-%s->' % machine)
        for point in args[machine]:
            print('<--设定%s-->' % point)
            for name in args[machine][point]:
                current_value = args[machine][point][name]
                print("[%s-%s-%s]当前设定值为:%s" % (machine, point, name, current_value))
                new_value = input('修改为(按回车跳过):')
                if new_value != '':
                    args[machine][point][name] = int(new_value)
                else:
                    print('未修改')
            print('<!--设定%s完成-->' % point)
        print('<!-%s->' % machine)
    print('设定完成，正在上传...')
    res = requests.put(server+'/hardware/arguments', headers=header, data={'machine_id': machine_id,
                                                                          'arguments': json.dumps(args)})
    if res.json()['flag']:
        input('修改成功，按回车键退出')
        exit()
    else:
        input('修改失败，按回车键退出')
        exit()
else:
    print('网球机%s无参数设置，将新增参数' % machine_id)
    args = {
        'machineA': {},
        'machineB': {}
    }
    for machine in args:
        print('<-%s->' % machine)
        for i in range(1,17):
            point = 'point%s'%i
            print('<--设定%s-->' % point)
            args[machine][point] = {}
            value = input("[%s-%s-upspeed]设置为:"%(machine,point))
            args[machine][point]['upspeed'] = int(value)
            value = input("[%s-%s-downspeed]设置为:"%(machine,point))
            args[machine][point]['downspeed'] = int(value)
            value = input("[%s-%s-vertical]设置为:"%(machine,point))
            args[machine][point]['vertical'] = int(value)
            value = input("[%s-%s-horizontal]设置为:"%(machine,point))
            args[machine][point]['horizontal'] = int(value)
            print('<!--设定%s完成-->' % point)
        print('<!-%s->' % machine)
    res = requests.post(server+'/hardware/arguments', headers=header, data={'machine_id': machine_id,
                                                                           'arguments': json.dumps(args)})
    if res.json()['flag']:
        input('修改成功，按回车键退出')
        exit()
    else:
        input('修改失败，按回车键退出')
        exit()









