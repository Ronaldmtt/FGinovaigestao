bind = "0.0.0.0:5000"
workers = 1
worker_class = "sync"
timeout = 300  # 5 minutos para processos longos de IA
keepalive = 60
reload = True
preload_app = False
reuse_port = True