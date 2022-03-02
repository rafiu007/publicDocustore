from distutils.command.upload import upload
from operator import index
from pyexpat import model
from django.db import models


class Topics(models.Model):
    topic_name = models.CharField(max_length=120, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["created_at"]
        indexes = [models.Index(fields=["topic_name"])]


class FileUpload(models.Model):
    file_name = models.CharField(max_length=120)
    file = models.FileField(upload_to="upload/%Y/%m/%d/")
    file_topic = models.ManyToManyField(Topics, related_name="topics")
    file_type = models.CharField(max_length=50, default="txt")
    file_size = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.file_name

    class Meta:
        ordering = ["created_at"]
        indexes = [models.Index(fields=["file_name"])]


class Folder(models.Model):
    folder_name = models.CharField(max_length=120, blank=False)
    files_no = models.IntegerField(default=0)
    file = models.ManyToManyField(FileUpload, related_name="f2f")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.folder_name

    class Meta:
        ordering = ["created_at"]
