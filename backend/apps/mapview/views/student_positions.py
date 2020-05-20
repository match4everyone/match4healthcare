from django.http import JsonResponse

from apps.iamstudent.models import Student
from apps.mapview.src.map import group_by_zip_code


def supportersJSON(request):
    students = Student.objects.filter(user__validated_email=True)
    supporters = group_by_zip_code(students)
    return JsonResponse(supporters)
