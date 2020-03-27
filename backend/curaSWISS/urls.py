"""curaSWISS URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from curaSWISS import views
from curaSWISS.settings import common as settings
from django.contrib.staticfiles.storage import staticfiles_storage
from django.views.generic.base import RedirectView

urlpatterns = [
    path('mapview/', include('apps.mapview.urls')),
    path('iamstudent/', include('apps.iamstudent.urls')),
    path('ineedstudent/', include('apps.ineedstudent.urls')),
    path('accounts/', include('apps.accounts.urls')),
    path('admin/', admin.site.urls),
    path('', views.home),
    path('about/', views.about),
    path('impressum/', views.impressum),
    path('dataprotection/', views.dataprotection),
    path('legal-questions/', views.legal_questions),
    path('android-icon-144x144.png', RedirectView.as_view(url=staticfiles_storage.url('img/favicon/android-icon-144x144.png'))),
    path('android-icon-192x192.png', RedirectView.as_view(url=staticfiles_storage.url('img/favicon/android-icon-192x192.png'))),
    path('android-icon-36x36.png', RedirectView.as_view(url=staticfiles_storage.url('img/favicon/android-icon-36x36.png'))),
    path('android-icon-48x48.png', RedirectView.as_view(url=staticfiles_storage.url('img/favicon/android-icon-48x48.png'))),
    path('android-icon-72x72.png', RedirectView.as_view(url=staticfiles_storage.url('img/favicon/android-icon-72x72.png'))),
    path('android-icon-96x96.png', RedirectView.as_view(url=staticfiles_storage.url('img/favicon/android-icon-96x96.png'))),
    path('apple-icon-114x114.png', RedirectView.as_view(url=staticfiles_storage.url('img/favicon/apple-icon-114x114.png'))),
    path('apple-icon-120x120.png', RedirectView.as_view(url=staticfiles_storage.url('img/favicon/apple-icon-120x120.png'))),
    path('apple-icon-144x144.png', RedirectView.as_view(url=staticfiles_storage.url('img/favicon/apple-icon-144x144.png'))),
    path('apple-icon-152x152.png', RedirectView.as_view(url=staticfiles_storage.url('img/favicon/apple-icon-152x152.png'))),
    path('apple-icon-180x180.png', RedirectView.as_view(url=staticfiles_storage.url('img/favicon/apple-icon-180x180.png'))),
    path('apple-icon-57x57.png', RedirectView.as_view(url=staticfiles_storage.url('img/favicon/apple-icon-57x57.png'))),
    path('apple-icon-60x60.png', RedirectView.as_view(url=staticfiles_storage.url('img/favicon/apple-icon-60x60.png'))),
    path('apple-icon-72x72.png', RedirectView.as_view(url=staticfiles_storage.url('img/favicon/apple-icon-72x72.png'))),
    path('apple-icon-76x76.png', RedirectView.as_view(url=staticfiles_storage.url('img/favicon/apple-icon-76x76.png'))),
    path('apple-icon-precomposed.png', RedirectView.as_view(url=staticfiles_storage.url('img/favicon/apple-icon-precomposed.png'))),
    path('apple-icon.png', RedirectView.as_view(url=staticfiles_storage.url('img/favicon/apple-icon.png'))),
    path('favicon-16x16.png', RedirectView.as_view(url=staticfiles_storage.url('img/favicon/favicon-16x16.png'))),
    path('favicon-32x32.png', RedirectView.as_view(url=staticfiles_storage.url('img/favicon/favicon-32x32.png'))),
    path('favicon-96x96.png', RedirectView.as_view(url=staticfiles_storage.url('img/favicon/favicon-96x96.png'))),
    path('favicon.ico', RedirectView.as_view(url=staticfiles_storage.url('img/favicon/favicon.ico'))),
    path('ms-icon-144x144.png', RedirectView.as_view(url=staticfiles_storage.url('img/favicon/ms-icon-144x144.png'))),
    path('ms-icon-150x150.png', RedirectView.as_view(url=staticfiles_storage.url('img/favicon/ms-icon-150x150.png'))),
    path('ms-icon-310x310.png', RedirectView.as_view(url=staticfiles_storage.url('img/favicon/ms-icon-310x310.png'))),
    path('ms-icon-70x70.png', RedirectView.as_view(url=staticfiles_storage.url('img/favicon/ms-icon-70x70.png')))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()
