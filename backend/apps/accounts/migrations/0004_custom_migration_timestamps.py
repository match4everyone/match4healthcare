from django.db import migrations, transaction
import logging
from datetime import datetime
logger = logging.getLogger("django")

def update_emails(apps, schema_editor):
    User = apps.get_model('accounts', 'User')


    for user in User.objects.all():
        if user.registration_date:
            logger.warn("user has registration_date")
            continue

        user.registration_date = datetime.now()
        user.save()


    for user in User.objects.all():
        if user.email_validation_date:
            logger.warn("user has validation_date")
            continue

        if user.validated_email:
            user.email_validation_date = datetime.now()
            user.save()


class Migration(migrations.Migration):
    atomic = False

    dependencies = [
        ('accounts', '0003_user_registration_date'),
    ]

    operations = [
        migrations.RunPython(update_emails),
    ]
