import urllib2
import uuid
import os
import json

from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

import classification

classifier = classification.load_model()
labels_all = classification.get_labels()


def fileupload_view(request):
    if request.method == "POST":
        error = 0
        pred = None
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
            print img_url
            file_path = 'AppServer/static/assets/img/'+ str(uuid.uuid1()) + '.jpg'
            try:
                destination = open(file_path, 'w+')
                string_buffer = urllib2.urlopen(img_url).read()
                destination.write(string_buffer)
                destination.close()
            except Exception as e:
                print "can not download image"
                print e
                error = 1
            img_link = img_url

        if not error:
            pred = classification.get_predict_labels(file_path, classifier, labels_all)
        return render(request, 'fileuploader.html', {'pred':pred, 'img_link': img_link, 'uploaded': 1, 'error': error})
    else:
        return render(request, 'fileuploader.html', {})


@csrf_exempt
def classifyimage_view(request):
    if request.method == "POST":
        label = []
        image_path = request.POST["photo_path"]
        if not os.path.isfile(image_path):
            print 'Photo %s not found' % image_path
            return HttpResponse('Photo not found!', status=400)

        pred = classification.get_predict_labels(image_path, classifier, labels_all)
        if(pred[0][1] < 0.77):
            print pred[0][1]
            print 'Cannot Recognize photo %s' % image_path
            return HttpResponse('Cannot Recognize photo!', status=400)
        for item in pred:
            label.append({'name': item[0], 'prob': item[1]})
        print label
        return HttpResponse(json.dumps(label), content_type="application/json")
