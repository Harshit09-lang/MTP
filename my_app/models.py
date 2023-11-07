from django.db import models

# Create your models here.
class Data(models.Model):
    data = models.FileField(upload_to="data_file")

class MLmodel(models.Model):
    ml_file = models.FileField(upload_to="ml_model")