FROM ubuntu:18.04

RUN apt-get update && apt-get install -y python3 python3-pip libpq-dev gettext
WORKDIR /match4healthcare-backend
COPY requirements.txt /match4healthcare-backend/requirements.txt
RUN pip3 install -r requirements.txt
COPY requirements.prod.txt /match4healthcare-backend/requirements.prod.txt
RUN pip3 install -r requirements.prod.txt

EXPOSE 8000
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
