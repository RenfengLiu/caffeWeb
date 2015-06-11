
from django.shortcuts import render, redirect                                                                                      
from django.http import Http404, HttpResponse
import classification 

classifier = classification.load_model()
labels_all = classification.get_labels()


def fileupload_view(request):

    if request.method == "POST":
        uploaded_file = request.FILES['meal_photo']
        file_path = uploaded_file.name
        destination = open(file_path, 'wb+')
        for chunk in uploaded_file.chunks():
        	destination.write(chunk)
        destination.close()
        	
        pred = classification.get_predict_labels(file_path, classifier, labels_all)
        photo.pred = pred
        photo.file_path = file_path
        return render(request, 'fileuploader.html', {'photo':photo, 'uploaded':1})
    else:    
    	return render(request, 'fileuploader.html', {})

