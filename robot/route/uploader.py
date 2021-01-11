import json
from threading import Thread

from django.http import JsonResponse
from django.shortcuts import render
from robot import compass, models


def uploaderGet(request):
    return render(request, 'uploader.html', {
        'profile': models.ChromeProfile.objects.all(),
        'collection': models.CSVCollection.objects.all()
        })


def uploaderPost(request):
    if request.is_ajax():
        from robot.route.mobile import triggerByThread
        args = compass(json.loads(request.body))
        profile_path = models.ChromeProfile.objects.get(pk=args.profile).path
        file_path = models.CSVCollection.objects.get(pk=args.collection).path

        # trigger = Thread(target=triggerByThread, args=(profile_path, str(file_path)))
        trigger = Thread(target=triggerByThread, args=(profile_path, ))
        trigger.start()

    return JsonResponse({'notify': 'ok'})
