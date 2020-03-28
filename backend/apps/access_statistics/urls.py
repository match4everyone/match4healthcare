from django.urls import path, include


urlpatterns = [
    path('access_statistics', views.access_statistics, name='access_statistics'),
]
