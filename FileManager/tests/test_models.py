from django.test import TestCase
from FileManager.models import FileUpload
from FileManager.models import Folder
from FileManager.models import Topics

class TestFileManagerModels(TestCase):

    def test_FileUpload_model_str(self):
        file_name = FileUpload.objects.create(file_name = "FileUpload Model Testing")
        self.assertEqual(str(file_name), "FileUpload Model Testing")


    def test_Folder_model(self):
        folder_name = Folder.objects.create(folder_name = "Folder Model Testing")
        self.assertEqual(str(folder_name), "Folder Model Testing")