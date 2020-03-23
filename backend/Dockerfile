FROM ubuntu:18.04

RUN apt-get update && apt-get install -y python3 python3-pip libpq-dev gettext
WORKDIR /matchmedisvsvirus-backend
COPY requirements.txt /matchmedisvsvirus-backend/requirements.txt
RUN pip3 install -r requirements.txt

EXPOSE 8000
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
