from AppServer.models import UserRecord, GlucoseRecord, MealRecord, SleepRecord, A1CHistory, Comment, \
                             ExerciseRecord, Recommendation, UserStatus, NoteRecord, PhotoUploaded, \
                             WeightHistory, StatusRecord, PhotoTag, RefPhotoRecommendation,RefTagCategory, \
                             RefTagcategoryRecommenation, PhotoPredTags



import classification 

classifier = classification.load_model()
labels_all = classification.get_labels()
classifier_ver = 1

photos = PhotoUploaded.objects.all()
for photo in photos:
    pred = classification.get_predict_labels(photo.file_path, classifier, labels_all)
    if photo.pred == None:
        pred_tags=PhotoPredTags(tag1=pred[0][0], prob1=pred[0][1],
                tag2=pred[1][0], prob2=pred[1][1],
                tag3=pred[2][0], prob3=pred[2][1],
                tag4=pred[3][0], prob4=pred[3][1],
                tag5=pred[4][0], prob5=pred[4][1], modeleversion=classifier_ver)
        pred_tags.save()
        photo.pred = pred_tags
        photo.save()
    else:
        photo.pred.tag1  = pred[0][0]
        photo.pred.prob1 = pred[0][1]
        photo.pred.tag2  = pred[1][0]
        photo.pred.prob2 = pred[1][1]
        photo.pred.tag3  = pred[2][0]
        photo.pred.prob3 = pred[2][1]
        photo.pred.tag4  = pred[3][0]
        photo.pred.prob4 = pred[3][1]
        photo.pred.tag5  = pred[4][0]
        photo.pred.prob5 = pred[4][1]
        photo.pred.modeleversion = classifier_ver
        photo.pred.save()
    photo.save()

