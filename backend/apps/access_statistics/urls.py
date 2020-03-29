from django.urls import path, include
from . import views


urlpatterns = [
    path('view', views.access_statistics, name='access_statistics'),
]
