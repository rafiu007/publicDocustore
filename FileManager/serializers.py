# from importlib.metadata import files
# from typing import Type
from rest_framework import serializers
from .models import *

class TypesSerializers(serializers.ModelSerializer):
    class Meta:
        model=Topics
        fields = '__all__'

class FileSerializers(serializers.ModelSerializer):
    topics=TypesSerializers(many=True, read_only=True)
    class Meta:
        model = FileUpload
        fields = '__all__'

class FolderSerializers(serializers.ModelSerializer):
    filejs=FileSerializers(read_only=True,many=True)
    class Meta:
        model = Folder
        fields = '__all__'