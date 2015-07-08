import urllib2, StringIO
from django.shortcuts import render, redirect                                                                                      
from django.http import Http404, HttpResponse
import uuid
import os
import classification   
classifier = classification.load_model()
labels_all = classification.get_labels()

def fileupload_view(request):
    if request.method == "POST":
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
                print "can not download image..."
            img_link = img_url

        pred = classification.get_predict_labels(file_path, classifier, labels_all)
        file_path = 'assets/img/' + file_name
        return render(request, 'fileuploader.html', {'pred':pred, 'img_link':img_link, 'uploaded':1})
    else:    
    	return render(request, 'fileuploader.html', {})

