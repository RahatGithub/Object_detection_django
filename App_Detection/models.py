from django.db import models

class TestMedia(models.Model):
    id = models.AutoField(primary_key=True)
    file = models.FileField(upload_to='uploaded_files', blank=True) 