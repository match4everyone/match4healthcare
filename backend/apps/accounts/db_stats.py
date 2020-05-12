import datetime

from django.db.models import Count
from django.utils.translation import gettext_lazy as _

from apps.iamstudent.forms import form_labels
from apps.iamstudent.models import AUSBILDUNGS_TYPEN_COLUMNS, EmailToHospital, EmailToSend, Student
from apps.ineedstudent.models import Hospital

from .models import Newsletter, User


class RegisterList(list):
    def register(self, method):
        self.append(method)
        return method


class DataBaseStats:

    stat_count = RegisterList()
    stat_list = RegisterList()

    # TODO: last X days? # noqa: T003

    length_history_days = 7

    @stat_count.register
    def admin_count(self):
        return (
            _("Aktive Staffmember"),
            User.objects.filter(is_staff=True).count(),
            (
                [
                    datetime.date.today() - datetime.timedelta(days=i)
                    for i in range(self.length_history_days, 0 - 1, -1)
                ],
                [
                    User.objects.filter(
                        is_staff=True,
                        # __lte "less than or equal"
                        date_joined__lte=str(datetime.date.today() - datetime.timedelta(days=i)),
                    ).count()
                    for i in range(self.length_history_days, 0 - 1, -1)
                ],
            ),
        )

    @stat_count.register
    def approved_hospital_count(self):
        return (
            _("Akzeptierte Institutionen"),
            Hospital.objects.filter(is_approved=True, user__validated_email=True).count(),
            (
                [
                    datetime.date.today() - datetime.timedelta(days=i)
                    for i in range(self.length_history_days, 0 - 1, -1)
                ],
                [
                    Hospital.objects.filter(
                        is_approved=True,
                        user__validated_email=True,
                        approval_date__lte=str(datetime.date.today() - datetime.timedelta(days=i)),
                    ).count()
                    for i in range(self.length_history_days, 0 - 1, -1)
                ],
            ),
        )

    @stat_count.register
    def validated_student_count(self):
        return (
            _("Registrierte Helfende"),
            Student.objects.filter(user__validated_email=True).count(),
            (
                [
                    datetime.date.today() - datetime.timedelta(days=i)
                    for i in range(self.length_history_days, 0 - 1, -1)
                ],
                [
                    Student.objects.filter(
                        user__validated_email=True,
                        user__date_joined__lte=str(
                            datetime.date.today() - datetime.timedelta(days=i)
                        ),
                    ).count()
                    for i in range(self.length_history_days, 0 - 1, -1)
                ],
            ),
        )

    @stat_count.register
    def deactivated_accounts(self):
        return (
            _("Anzahl deaktivierter Helfenden"),
            Student.objects.filter(is_activated=False).count(),
            (None, None),
        )

    # TODO: helfende pro bundesland und großstadt. Requires
    # https://github.com/match4everyone/match4healthcare/issues/492

    # Contact stats
    @stat_count.register
    def emails_to_students(self):
        return (
            _("Kontaktanfragen an Helfende"),
            EmailToSend.objects.filter(was_sent=True).count(),
            (
                [
                    datetime.date.today() - datetime.timedelta(days=i)
                    for i in range(self.length_history_days, 0 - 1, -1)
                ],
                [
                    EmailToSend.objects.filter(
                        was_sent=True,
                        send_date__lte=str(datetime.date.today() - datetime.timedelta(days=i)),
                    ).count()
                    for i in range(self.length_history_days, 0 - 1, -1)
                ],
            ),
        )

    @stat_count.register
    def emails_to_hospitals(self):
        return (
            _("Kontaktanfragen an Institutionen"),
            EmailToHospital.objects.count(),
            (
                [
                    datetime.date.today() - datetime.timedelta(days=i)
                    for i in range(self.length_history_days, 0 - 1, -1)
                ],
                [
                    EmailToHospital.objects.filter(
                        send_date__lte=str(datetime.date.today() - datetime.timedelta(days=i))
                    ).count()
                    for i in range(self.length_history_days, 0 - 1, -1)
                ],
            ),
        )

    @stat_count.register
    def newsletter_count(self):
        return (
            _("Anzahl gesendeter Newsletter"),
            Newsletter.objects.filter(was_sent=True).count(),
            (
                [
                    datetime.date.today() - datetime.timedelta(days=i)
                    for i in range(self.length_history_days, 0 - 1, -1)
                ],
                [
                    Newsletter.objects.filter(
                        was_sent=True,
                        send_date__lte=str(datetime.date.today() - datetime.timedelta(days=i)),
                    ).count()
                    for i in range(self.length_history_days, 0 - 1, -1)
                ],
            ),
        )

    @stat_count.register
    def hospitals_allowing_contact_by_students(self):
        return (
            _("Institutionen mit Anzeige"),
            Hospital.objects.filter(
                is_approved=True, user__validated_email=True, appears_in_map=True
            ).count(),
            (None, None),
        )

    @stat_list.register
    def berufsgruppen(self):
        res = []
        for t in AUSBILDUNGS_TYPEN_COLUMNS:
            qs = (
                Student.objects.filter(user__validated_email=True)
                .values(t)
                .annotate(total=Count("user_id"))
                .order_by(t)
            )
            try:
                count = next(x for x in qs if x[t] is True)["total"]
            except StopIteration:
                count = 0
            res.append((form_labels[t], count, (None, None)))
        return res

    def all_stats(self):
        results = [m(self) for m in self.stat_count]
        for m in self.stat_list:
            results.extend(m(self))
        return results
