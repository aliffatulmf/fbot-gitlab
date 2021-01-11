import csv
import json
import os
import pathlib
import platform
import shutil
import signal
import uuid
import datetime
from threading import Thread

from django.db.transaction import atomic
from django.db.utils import IntegrityError
from django.http.response import Http404, HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.urls.base import reverse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from fbot.settings import BASE_DIR

from robot import *
from robot import CONFIG_DIR, separator
from robot.forms import CSVCollectionForm
from robot.models import ChromeProfile, CSVCollection
from robot.profiles.profiles import login_session, make_profile
from robot.route.mobile import Driver, Mobile, interface
from robot.utils import Util


class Files(View):
    UTIL = Util()

    def write_file(self, filename):
        with open(filename, mode="w", encoding="utf-8", newline="") as cfile:
            fields = ["NAME", "PRICE", "IMAGES", "CATEGORY", "LOCATION", "DESCRIPTION"]

            wf = csv.DictWriter(cfile, fieldnames=fields)
            wf.writeheader()

        return filename

    def get(self, request):
        data = CSVCollection.objects.all()
        return render(request, "csv_upload.html", {"data": data})

    @atomic
    def post(self, request):
        filename = str(uuid.uuid4()).replace("-", "") + ".csv"
        filepath = Util.files_dir + "/" + filename

        name = request.POST["name"]
        path = self.write_file(filepath)

        try:
            query = CSVCollection(name=name, filename=filename, path=path)
            query.save()
        except:
            self.UTIL.remove_file(filepath)
            return HttpResponse("<h1>Error</h1>")

        return redirect(reverse("csv_upload"))

    @atomic
    def delete(self, request):
        data = json.loads(request.body)

        try:

            query = CSVCollection.objects.get(pk=data["id"])
            remove = self.UTIL.remove_file(str(query.path))

            if remove:
                query.delete()

        except Exception as e:
            return JsonResponse({"msg": "ERROR"})

        return JsonResponse({"msg": "SUCCESS"})


class Profile(View):
    UTIL = Util()

    def get(self, request):
        data = ChromeProfile.objects.all()
        return render(request, "chrome_profile.html", {"data": data})

    @atomic
    def post(self, request):
        name = request.POST.get("name")
        path = self.UTIL.create(name, self.UTIL.run)
        try:
            data = ChromeProfile(name=name, path=path)
            data.save()
        except IntegrityError as e:
            raise Http404(e)
        return redirect(reverse("chrome_profile"))

    @atomic
    def delete(self, request):
        try:
            body = json.loads(request.body)
            data = ChromeProfile.objects.get(pk=body["id"])

            if data.path:
                action = self.UTIL.delete(data.path)

                if action:
                    data.delete()

        except IntegrityError as e:
            raise Http404(e)

        return JsonResponse({"msg": "SUCCESS"})


def chromeProfileLogin(request):
    body = json.loads(request.body)

    data = ChromeProfile.objects.get(pk=body["id"])
    print("starting")
    Util().run(pathlib.Path(data.path))
    print("executed")
    return JsonResponse({"msg": "OK"})


class Control(View):
    UTIL = Util()

    def get(self, request):
        data = {
            "profiles": ChromeProfile.objects.all(),
            "files": CSVCollection.objects.all(),
        }

        return render(request, "uploader.html", data)

    def post(self, request):
        try:
            DATA = json.loads(request.body)
            PROFILE = ChromeProfile.objects.get(pk=DATA["profile"])
            FILE = CSVCollection.objects.get(pk=DATA["file"])

            thread = Thread(target=interface, args=(PROFILE.path, FILE))
            thread.start()
        except Exception as e:
            return JsonResponse({"status": "error", "msg": "Error"})

        return JsonResponse({"status": "success", "msg": "OK"})
