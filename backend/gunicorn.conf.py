import multiprocessing

bind = "backend:8000"
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "gevent"
worker_connections = 1000

accesslog = 'access-logfile gunicorn-access-logfile-match4healthcare.txt'
access_log_format = '%(t)s|"%(r)s"|%(s)s|%(T)s'