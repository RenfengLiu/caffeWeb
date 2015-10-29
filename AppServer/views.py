import urllib2
import uuid
import os
import json

from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from models import ClassificationResults
from django.utils import timezone

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


def save_classification_result(image_path, pred, threshold):
    try:
        cls_ret = ClassificationResults.objects.get(image_path=image_path)
    except ClassificationResults.DoesNotExist:
        cls_ret = ClassificationResults()

    cls_ret.image_path = image_path
    cls_ret.upload_date = timezone.now()
    cls_ret.is_food = pred[0]['prob'] >= threshold
    cls_ret.threshold = threshold

    cls_ret.label1 = pred[0]['name']
    cls_ret.prob1 = pred[0]['prob']
    cls_ret.label2 = pred[1]['name']
    cls_ret.prob2 = pred[1]['prob']
    cls_ret.label3 = pred[2]['name']
    cls_ret.prob3 = pred[2]['prob']
    cls_ret.label4 = pred[3]['name']
    cls_ret.prob4 = pred[3]['prob']
    cls_ret.label5 = pred[4]['name']
    cls_ret.prob5 = pred[4]['prob']
    cls_ret.save()



@csrf_exempt
def classifyimage_view(request):
    if request.method == "POST":
        label = []
        image_path = request.POST["photo_path"]
        if not os.path.isfile(image_path):
            print 'Photo %s not found' % image_path
            return HttpResponse('Photo not found!', status=400)

        pred = classification.get_predict_labels(image_path, classifier, labels_all)

        for item in pred:
            label.append({'name': item[0], 'prob': item[1]})
        print label
        threshold = 0.37
        save_classification_result(image_path, label, threshold)
        if pred[0][1] < threshold:
            print pred[0][1]
            print 'Cannot Recognize photo %s' % image_path
            return HttpResponse('Cannot Recognize photo!', status=400)

        return HttpResponse(json.dumps(label), content_type="application/json")


def cls_results_view(request):
    results = ClassificationResults.objects.all().order_by('-upload_date')
    print results[0].image_path
    ret = []

    for result in results:
        result.image_path = result.image_path.replace('/var/www/GlucoGuide/production/source/services/entryPoint/public/', '/static/')
        ret.append(result)

    return render(request, 'results.html', {'results': results})
