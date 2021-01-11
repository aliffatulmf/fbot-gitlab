from django.conf import settings
from django.conf.urls.static import static
from django.http import *
from django.shortcuts import redirect
from django.urls import path
from django.urls.base import reverse

from robot.book import *
from robot.route.mobile import Mobile

urlpatterns = [
    path(r"", lambda request: redirect(reverse("chrome_profile")), name="dashboard"),
    path(r"profile/", Profile.as_view(), name="chrome_profile"),
    path(r"profile-login/", chromeProfileLogin, name="chrome_login"),
    path(r"csv-upload/", Files.as_view(), name="csv_upload"),
    path(r"uploader/", Control.as_view(), name="uploadControl"),
]
