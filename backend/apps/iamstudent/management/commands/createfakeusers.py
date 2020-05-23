from datetime import datetime, timedelta

from django.core.management.base import BaseCommand
import numpy as np

from apps.accounts.models import User
from apps.iamstudent.models import AUSBILDUNGS_TYPEN_COLUMNS, Student
from apps.ineedstudent.models import Hospital

from ._utils import BIG_CITY_PLZS

FAKE_MAIL = "@example.com"


def new_mail(x):
    return ("%s" % x) + FAKE_MAIL


class Command(BaseCommand):
    # has to be "help" because we inherit from django manage.py Command, thus ignore A003
    help = "Populates the database with fake users or deletes them."  # noqa: A003

    def add_arguments(self, parser):

        parser.add_argument(
            "--delete",
            action="store_true",
            help='Delete all users with an email ending in "%s"' % FAKE_MAIL,
        )

        parser.add_argument(
            "--add-students", nargs=1, help="Add [N] new students to the poll",
        )

        parser.add_argument(
            "--add-hospitals", nargs=1, help="Add [N] new hospitals to the poll",
        )

        parser.add_argument(
            "--no-input", action="store_true", help="Answer yes to all questions.",
        )

    def handle(self, *args, **options):
        if (
            not options["delete"]
            and options["add_hospitals"] is None
            and options["add_students"] is None
        ):
            self.print_help("", "")
            return None

        self.all_yes = options["no_input"]

        if options["delete"]:
            self.delete_all_fakes()
        if options["add_hospitals"] is not None:
            self.add_fake_hospitals(int(options["add_hospitals"][0]))
        if options["add_students"] is not None:
            self.add_fake_students(int(options["add_students"][0]))

    def delete_all_fakes(self):
        qs = User.objects.filter(email__contains=FAKE_MAIL)

        n = qs.count()
        if n == 0:
            self.stdout.write(self.style.SUCCESS("No fake users detected."))
            return

        is_sure = (
            input(
                'You are about to delete %s users with emails including "%s". '
                "Are you sure you want to delete them? [y/n]" % (n, FAKE_MAIL)
            )
            if not self.all_yes
            else "y"
        )
        if is_sure != "y":
            self.stdout.write(self.style.WARNING("Users NOT deleted."))
            return

        qs.delete()
        self.stdout.write(self.style.SUCCESS("Successfully deleted these %s fake users." % n))

    def add_fake_students(self, n):
        plzs = np.random.choice(BIG_CITY_PLZS, size=n)
        months = np.random.choice(np.arange(1, 12), size=n)
        days = np.random.choice(np.arange(2, 15), size=n)
        year = 2020
        n_users = User.objects.all().count()

        for i in range(n):
            m = new_mail(i + n_users)
            kwd = dict(
                zip(
                    AUSBILDUNGS_TYPEN_COLUMNS,
                    np.random.choice([True, False], size=len(AUSBILDUNGS_TYPEN_COLUMNS)),
                )
            )

            u = User.objects.create(
                username=m,
                email=m,
                is_student=True,
                validated_email=True,
                date_joined=datetime.now() - timedelta(days=np.random.randint(0, 30)),
            )
            u.set_password(m)
            u.save()
            Student.objects.create(
                user=u,
                plz=plzs[i],
                braucht_bezahlung=np.random.choice([1, 2, 3]),
                is_activated=np.random.choice([True, False], p=[0.95, 0.05]),
                einwilligung_agb=True,
                datenschutz_zugestimmt=True,
                einwilligung_datenweitergabe=True,
                availability_start="{}-{:02d}-{:02d}".format(year, months[i], days[i]),
                zeitliche_verfuegbarkeit=np.random.choice([1, 2, 3, 4]),
                umkreis=np.random.choice([1, 2, 3, 4], p=[0.2, 0.5, 0.27, 0.03]),
                unterkunft_gewuenscht=np.random.choice([True, False], p=[0.1, 0.9]),
                **kwd
            )

        self.stdout.write(self.style.SUCCESS("Created %s students." % n))

    def add_fake_hospitals(self, n):
        plzs = np.random.choice(BIG_CITY_PLZS, size=n)
        n_users = User.objects.all().count()
        for i in range(n):
            m = new_mail(i + n_users)
            u = User.objects.create(
                username=m,
                email=m,
                is_student=True,
                validated_email=True,
                date_joined=datetime.now() - timedelta(days=np.random.randint(0, 30)),
            )
            u.set_password(m)
            u.save()
            Hospital.objects.create(
                user=u,
                plz=plzs[i],
                ansprechpartner="Frau Müller",
                sonstige_infos="Wir haben viel zu tun.",
                is_approved=np.random.choice([True, False], p=[0.7, 0.3]),
                appears_in_map=np.random.choice([True, False], p=[0.8, 0.2]),
            )

        self.stdout.write(self.style.SUCCESS("Created %s hospitals." % n))
