from django.db import migrations, transaction
import logging

logger = logging.getLogger("django")

def update_emails(apps, schema_editor):
    EmailToSend = apps.get_model('iamstudent', 'EmailToSend')
    EmailToHospital = apps.get_model('iamstudent', 'EmailToHospital')

    for email in EmailToSend.objects.all():
        if email.send_date:
            logger.warn("email has send_date")
            continue
        if email.was_sent:
            email.send_date = email.registration_date
            email.save()

    for email in EmailToHospital.objects.all():
        if email.send_date:
            logger.warn("email has send_date")
            continue
        email.send_date = email.registration_date
        email.save()






class Migration(migrations.Migration):
    atomic = False

    dependencies = [
        ('iamstudent', '0015_auto_20200409_1620'),
    ]

    operations = [
        migrations.RunPython(update_emails),
    ]
