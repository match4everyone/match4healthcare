from django.db import migrations, transaction
import logging

def update_emails(apps, schema_editor):
    EmailToSend = apps.get_model('iamstudent', 'EmailToSend')
    EmailGroup = apps.get_model('iamstudent', 'EmailGroup')

    with transaction.atomic():

        groups = {}

        for email in EmailToSend.objects.all():
            truetext = "\n".join(email.message.split("wir haben folgende Nachricht von")[1].split("\n")[4:])

            if not email.hospital in groups:
                groups[email.hospital] = {}

            if not truetext in groups[email.hospital]:
                email_group = EmailGroup.objects.create(
                    subject=email.subject,
                    message=truetext,
                    hospital=email.hospital,
                    registration_date=email.registration_date
                )
                email_group.save()
                groups[email.hospital][truetext] = email_group

            email.email_group = groups[email.hospital][truetext]
            email.message = truetext
            email.save()


class Migration(migrations.Migration):
    atomic = False

    operations = [
        migrations.RunPython(update_emails),
    ]
