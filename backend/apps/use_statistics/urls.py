from django.urls import path, include
from . import views


urlpatterns = [
    path('view', views.use_statistics, name='use_statistics'),
]
