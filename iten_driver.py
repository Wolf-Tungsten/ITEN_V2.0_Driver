from tornado.options import options, define
from iten_model import Machine

define("id", default='TEST1', help="网球机id", type=str)
define("server", default='http://wolf.myseu.cn:5197/itenserv', help="服务器地址", type=str)
define("com", default='/dev/ttys0', help="串口名称", type=str)
define("enable_cv", default=True, help="是否启用视觉", type=str)
options.parse_command_line()

machine = Machine.Machine(machine_id=options.id,
                          server=options.server,
                          com=options.com,
                          camera='')
