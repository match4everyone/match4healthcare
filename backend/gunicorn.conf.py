import multiprocessing, os
from match4healthcare.settings.common import RUN_DIR

bind = "backend:8000"
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "gevent"
worker_connections = 1000

accesslog = os.path.join(RUN_DIR, 'gunicorn-access.log')
access_log_format = '%(t)s|"%(r)s"|%(s)s|%(D)s'