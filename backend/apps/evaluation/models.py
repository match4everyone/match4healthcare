from django.db import models


class StudentEvaluation(models.Model):
    test = models.CharField(max_length=50, default='')
