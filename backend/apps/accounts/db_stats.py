import datetime

from django.db.models import Count
from django.utils.translation import gettext_lazy as _

from apps.iamstudent.forms import form_labels
from apps.iamstudent.models import AUSBILDUNGS_TYPEN_COLUMNS, EmailToHospital, EmailToSend, Student
from apps.ineedstudent.models import Hospital

from .models import Newsletter, User


class RegisterList(list):
    def register_named(self, name, method):
        self.append((name, method))
        return method

    def register(self, name):
        return lambda func: self.register_named(name, func)


class DataBaseStats:
    stat_count = RegisterList()
    stat_list = RegisterList()
    dated_count = RegisterList()

    # TODO: last X days? # noqa: T003

    def __init__(self, length_history_days=7):
        self.length_history_days = length_history_days

    def day_interval(self, i):
        return datetime.date.today() - datetime.timedelta(days=i)

    def day_range(self):
        return range(self.length_history_days, 0 - 2, -1)

    def generate_cum_graph(self, count_func):
        return (
            [self.day_interval(i) for i in self.day_range()],
            [count_func(self, date=self.day_interval(i)) for i in self.day_range()],
        )

    @stat_count.register(name=_("Aktive Staffmember"))
    def admin_count(self, date=None):
        qs = User.objects.all()
        if date is not None:
            qs = qs.filter(date_joined__lte=str(date))
        return qs.filter(is_staff=True).count()

    @stat_count.register(name=_("Akzeptierte Institutionen"))
    def approved_hospital_count(self, date=None):
        qs = Hospital.objects.all()
        if date is not None:
            qs = qs.filter(approval_date__lte=str(date))
        return qs.filter(is_approved=True, user__validated_email=True).count()

    @stat_count.register(name=_("Registrierte Helfende"))
    def validated_student_count(self, date=None):
        qs = Student.objects.all()
        if date is not None:
            qs = qs.filter(user__date_joined__lte=str(date))
        return qs.filter(user__validated_email=True).count()

    @stat_count.register(name=_("Anzahl deaktivierter Helfenden"))
    def deactivated_accounts(self, date=None):
        # no dates are available for this
        return Student.objects.filter(is_activated=False).count()

    # TODO: helfende pro bundesland und großstadt. Requires
    # https://github.com/match4everyone/match4healthcare/issues/492

    # Contact stats
    @stat_count.register(name=_("Kontaktanfragen an Helfende"))
    def emails_to_students(self, date=None):
        qs = EmailToSend.objects.all()
        if date is not None:
            qs = qs.filter(send_date__lte=str(date))
        return qs.filter(was_sent=True).count()

    @stat_count.register(name=_("Kontaktanfragen an Institutionen"))
    def emails_to_hospitals(self, date=None):
        qs = EmailToHospital.objects.all()
        if date is not None:
            qs = qs.filter(send_date__lte=str(date))
        return qs.count()

    @stat_count.register(name=_("Anzahl gesendeter Newsletter"))
    def newsletter_count(self, date=None):
        qs = Newsletter.objects.all()
        if date is not None:
            qs = qs.filter(send_date__lte=str(date))

        return qs.filter(was_sent=True).count()

    @stat_count.register(name=_("Institutionen mit Anzeige"))
    def hospitals_allowing_contact_by_students(self, date=None):
        qs = Hospital.objects.all()

        if date is not None:
            qs = qs.filter(user__date_joined__lte=str(date))

        return qs.filter(is_approved=True, user__validated_email=True, appears_in_map=True).count()

    @stat_list.register(name="gruppen")
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
        results = [(description, count_func(self)) for description, count_func in self.stat_count]
        for name, m in self.stat_list:
            results.extend(m(self))
        return results

    def all_graphs(self):
        return [(name, self.generate_cum_graph(count_func)) for name, count_func in self.stat_count]
