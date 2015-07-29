import urllib2
import uuid
import os

from django.shortcuts import render
import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

import classification

classifier = classification.load_model()
labels_all = classification.get_labels()


def fileupload_view(request):
    if request.method == "POST":
        error = None
        file_source = request.POST["imgsource"]
        if file_source == "1":
            uploaded_file = request.FILES['meal_photo']
            filename, file_extension = os.path.splitext(uploaded_file.name)
            file_name = str(uuid.uuid1()) + file_extension
            file_path = 'AppServer/static/assets/img/' + file_name

            img_link = '/static/assets/img/' + file_name
            destination = open(file_path, 'w+')
            for chunk in uploaded_file.chunks():
                destination.write(chunk)
            destination.close()
        else:
            img_url = request.POST["imgurl"]
            file_path = 'AppServer/static/assets/img/'+ str(uuid.uuid1()) + '.jpg'
            file_name = 'tmp.jpg'
            try:
                destination = open(file_path, 'w+')
                string_buffer =urllib2.urlopen(img_url).read()
                destination.write(string_buffer)
                destination.close()
            except:
                print "can not download image"
                error = "can not download image."
            img_link = img_url

        pred = classification.get_predict_labels(file_path, classifier, labels_all)
        # file_path = 'assets/img/' + file_name
        return render(request, 'fileuploader.html', {'pred':pred, 'img_link': img_link, 'uploaded': 1, 'error': error})
    else:
        return render(request, 'fileuploader.html', {})

@csrf_exempt
def classifyimage_view(request):
    if request.method == "POST":
        lables = []
        image_path = request.POST["photo_path"]
        if os.path.isfile(image_path):
            print image_path

        pred = classification.get_predict_labels(image_path, classifier, labels_all)
        for item in pred:
            lables.append({'name': item[0], 'prob': item[1]})
        print lables
        return HttpResponse(json.dumps(lables), content_type="application/json")
