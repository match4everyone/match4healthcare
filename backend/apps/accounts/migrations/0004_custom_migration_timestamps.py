from django.db import migrations, transaction
import logging
from datetime import datetime
logger = logging.getLogger("django")

def update_emails(apps, schema_editor):
    User = apps.get_model('accounts', 'User')

    for user in User.objects.all():
        if user.email_validation_date:
            logger.warn("user has validation_date")
            continue

        if user.validated_email:
            user.email_validation_date = user.date_joined
            user.save()


class Migration(migrations.Migration):
    atomic = False

    dependencies = [
        ('accounts', '0002_user_email_validation_date'),
    ]

    operations = [
        migrations.RunPython(update_emails),
    ]
