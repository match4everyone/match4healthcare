import multiprocessing, os
from curaSWISS.settings.common import BASE_DIR

bind = "backend:8000"
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "gevent"
worker_connections = 1000

accesslog = os.path.join(BASE_DIR, 'run', 'gunicorn-access.log')
access_log_format = '%(t)s|"%(r)s"|%(s)s|%(T)s'