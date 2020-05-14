import logging

from django.http import JsonResponse
from rest_framework.views import APIView

from apps.accounts.modelss import User

logger = logging.getLogger(__name__)


class UserCountView(APIView):
    """
    A view that returns the count of active users.

    Source: https://stackoverflow.com/questions/25151586/django-rest-framework-retrieving-object-count-from-a-model
    """

    def get(self, request, format=None):  # noqa: A002
        supporter_count = User.objects.filter(
            is_student__exact=True, validated_email__exact=True
        ).count()
        facility_count = User.objects.filter(
            is_hospital__exact=True, validated_email__exact=True
        ).count()
        content = {"user_count": supporter_count, "facility_count": facility_count}
        return JsonResponse(content)
