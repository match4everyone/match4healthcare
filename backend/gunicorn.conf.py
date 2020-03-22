import multiprocessing

bind = "backend:8000"
workers = multiprocessing.cpu_count() * 3 + 1
