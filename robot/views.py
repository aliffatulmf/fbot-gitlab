import os
import shutil
from threading import Thread

from django.db import IntegrityError, transaction
from django.http import HttpResponse
from django.shortcuts import redirect, render, reverse
from django.views import View
from fbot.settings import BASE_DIR

from robot import forms, models
from robot.profiles.profiles import login_session, make_profile

FILES_PATH = str(BASE_DIR) + '/'


def profile(request):
    return render(request, 'master.html')


class firefox_profile(View):
    @transaction.atomic
    def get(self, request):
        query = models.FirefoxProfile.objects.all()

        if request.GET.get('cmd') == 'rm':
            fnd = models.FirefoxProfile.objects.get(pk=request.GET.get('id'))
            shutil.rmtree(fnd.path)
            fnd.delete()

        if request.GET.get('login') == 'true':
            path = models.FirefoxProfile.objects.get(pk=request.GET.get('id'))
            t = Thread(target=login_session, args=(path.path, ))
            t.start()

        return render(request, 'firefox_profile.html', {'data': query})

    @transaction.atomic
    def post(self, request):
        resolve = models.FirefoxProfile(name=request.POST.get('name'),
                                        path=make_profile(
                                            request.POST.get('name')))
        resolve.save()
        return redirect(reverse('firefox_profile'))


class csv_upload(View):
    def __init__(self):
        self.redirect = '/csv-upload/'

    def remove_file(self, obj):
        path = os.path.exists(FILES_PATH + str(obj.path))

        if path:
            os.remove(FILES_PATH + str(obj.path))
        else:
            return path

        return self.remove_file(obj)

    @transaction.atomic
    def get(self, request):
        query = models.CSVCollection.objects.all()

        if request.GET.get('cmd') == 'rm':
            fnd = models.CSVCollection.objects.get(pk=request.GET.get('id'))

            if self.remove_file(fnd) is False:
                fnd.delete()
            return redirect(self.redirect)

        return render(request, 'csv_upload.html', {'data': query})

    def post(self, request):
        query = forms.CSVCollection(request.POST, request.FILES)

        if query.is_valid():
            name = query.cleaned_data['name']
            path = query.cleaned_data['path']

            on_model = models.CSVCollection(name=name, path=path)

            try:
                with transaction.atomic():
                    on_model.save()
            except IntegrityError as e:
                return HttpResponse(e)

        return redirect(self.redirect)
