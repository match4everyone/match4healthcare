from ._utils import BIG_CITY_PLZS
import numpy as np
from apps.ineedstudent.models import Hospital
from apps.iamstudent.models import Student, AUSBILDUNGS_TYPEN_COLUMNS
from apps.accounts.models import User
from django.core.management.base import BaseCommand

FAKE_MAIL = "@example.com"
new_mail = lambda x: ("%s" % x) + FAKE_MAIL


class Command(BaseCommand):
    help = "Populates the database with fake users or deletes them."

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
        self.all_yes = options["no-input"]

        if options["delete"]:
            self.stdout.write(
                self.style.ERROR("Obviously, you cannot ADD and DELETE at the same time.")
            )
        if options["add-hospitals"] is not None:
            self.add_fakes(int(options["add-hospitals"][0]))
        if options["add-students"] is not None:
            self.add_fakes(int(options["add-students"][0]))

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

    def add_fakes(self, n):
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

            pwd = User.objects.make_random_password()
            u = User.objects.create(
                username=m, email=m, is_student=True, password=pwd, validated_email=True
            )
            s = Student.objects.create(
                user=u,
                plz=plzs[i],
                availability_start="{}-{:02d}-{:02d}".format(year, months[i], days[i]),
                **kwd
            )

        self.stdout.write(self.style.SUCCESS("Created %s students." % n))

    def add_fake_students(self, n):
        plzs = np.random.choice(BIG_CITY_PLZS, size=n)
        n_users = User.objects.all().count()
        for i in range(n):
            m = new_mail(i + n_users)
            pwd = User.objects.make_random_password()
            u = User.objects.create(
                username=m, email=m, is_student=True, password=pwd, validated_email=True
            )
            s = Hospital.objects.create(
                user=u,
                plz=plzs[i],
                ansprechpartner="Frau Müller",
                sonstige_infos="Wir haben viel zu tun.",
            )

        self.stdout.write(self.style.SUCCESS("Created %s hospitals." % n))
