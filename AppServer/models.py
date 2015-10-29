from django.db import models
# from datetime import datetime
from django.utils import timezone


# Create your models here.
class ClassificationResults(models.Model):
    image_path = models.CharField(max_length=200)
    upload_date = models.DateTimeField(default=timezone.now, blank=True)
    is_food = models.BooleanField(default=0)
    threshold = models.DecimalField(max_digits=10, decimal_places=2)
    label1 = models.CharField(max_length=20)
    prob1 = models.DecimalField(max_digits=10, decimal_places=2)
    label2 = models.CharField(max_length=20)
    prob2 = models.DecimalField(max_digits=10, decimal_places=2)
    label3 = models.CharField(max_length=20)
    prob3 = models.DecimalField(max_digits=10, decimal_places=2)
    label4 = models.CharField(max_length=20)
    prob4 = models.DecimalField(max_digits=10, decimal_places=2)
    label5 = models.CharField(max_length=20)
    prob5 = models.DecimalField(max_digits=10, decimal_places=2)

