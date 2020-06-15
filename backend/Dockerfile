FROM ubuntu:18.04

RUN apt-get update && apt-get install -y python3 python3-pip libpq-dev gettext

WORKDIR /match4everyone-backend
COPY requirements.txt /match4everyone-backend/requirements.txt
RUN pip3 install -r requirements.txt
COPY requirements.prod.txt /match4healthcare-backend/requirements.prod.txt
RUN pip3 install -r requirements.prod.txt

COPY . .
RUN django-admin makemessages --no-location --ignore 00_old_m4h_matching_code
RUN django-admin compilemessages
RUN python3 manage.py collectstatic --no-input

EXPOSE 8000
ENTRYPOINT ["./entrypoint.sh"]
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
