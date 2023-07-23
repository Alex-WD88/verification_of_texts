from django.db import models


class File(models.Model):
    name = models.CharField(max_length=255)
    document = models.FileField(upload_to='documents/')
    upload_date = models.DateTimeField(auto_now_add=True)


class Child_file(models.Model):
    parent_id = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    document = models.FileField(upload_to='documents/')
    upload_date = models.DateTimeField(auto_now_add=True)
