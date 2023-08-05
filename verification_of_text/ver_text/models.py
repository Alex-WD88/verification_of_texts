from django.db import models


class File(models.Model):
    name = models.CharField(max_length=255)
    document = models.FileField(upload_to='documents/')
    upload_date = models.DateTimeField(auto_now_add=True)


class ChildFile(models.Model):
    parent = models.ForeignKey(File, on_delete=models.CASCADE)
    document = models.FileField(upload_to='child_files/')
    name = models.CharField(max_length=200)
    upload_date = models.DateTimeField(auto_now_add=True)
