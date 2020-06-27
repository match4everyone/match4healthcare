FROM ubuntu:18.04

RUN apt-get update && apt-get install -y python3 python3-pip libpq-dev gettext

WORKDIR /backend
COPY requirements.txt /backend/requirements.txt
RUN pip3 install -r requirements.txt
COPY requirements.prod.txt /backend/requirements.prod.txt
RUN pip3 install -r requirements.prod.txt

COPY . .

RUN python3 manage.py makemessages --no-location --ignore 00_old_m4h_matching_code
RUN python3 manage.py compilemessages

# Change permissions on run/ in case app is later run by non-root user
# and delete log files as these are created during the above commands when django loads the configuration
# and will be created non writeable by others than root
RUN chmod -Rc a+rwX run && rm -v run/*log

EXPOSE 8000
ENTRYPOINT ["./entrypoint.sh"]
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
