"""d_services URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from rest_framework.routers import SimpleRouter

from services.token import ObtainAuthTokenAndUser
from services.views import *

api_urls = [
    url(r'^token-auth/$', ObtainAuthTokenAndUser.as_view()),
    url(r'^users/', UserAPIView.as_view(), name='user-list'),
    url(r'^free-washing-time/$',
        WashingTimeAPIView.as_view(),
        name='free-washing-time-list'),
    url(r'^free-washing-machines/$',
        FreeWashingMachinesAPIView.as_view(),
        name='free-washing-machines-list'),
    url(r'^washing-schedule/$',
        WashingScheduleAPIView.as_view(),
        name='washing-schedule-list'),
    url(r'^dormitories/$', DormitoryAPIView.as_view(), name='dormitory-list'),
    url(r'^staff-requests/$',
        StaffRequestAPIView.as_view(),
        name='staff-request-list'),
    url(r'^staff-requests/(?P<pk>\d+)/$',
        StaffRequestDetailAPIView.as_view(),
        name='staff-request-detail'),
]

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/', include(api_urls, namespace='api')),
]
