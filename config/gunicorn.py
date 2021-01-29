import multiprocessing

bind = '0.0.0.0:8000'
workers = multiprocessing.cpu_count() * 2 + 1

backlog = 2048
# 同步Worker: sync 默认模式, 也就是一次只处理一个请求
# 异步Worker: 通过 eventlet, gevent
# 异步IO Worker: 目前支持 gthread 和 gaiohttp 两种类型
# worker_class = "gevent"
# 使用于 gevent 和 eventlet 工作模式
worker_connections = 5000
# 守护进程模式运行, 放到后台运行
daemon = False

debug = True

# proc_name = 'backend_server1'
# pidfile = './log/gunicorn.pid'
# errorlog = './log/gunicorn.log'
