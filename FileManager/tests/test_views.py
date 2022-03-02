from django.test import TestCase
from FileManager.models import Topics
from FileManager.models import FileUpload
from FileManager.models import Folder


class TestViews(TestCase):
    def setUp(self):
        topicObject = Topics(topic_name="testTopic")
        topicObject.save()

        fileObject = FileUpload(
            file_name="testFile",
            file="/Users/rafiu/docuStore/FileManager/Data_for_tests/docs/120914674_1266836413655636_5862638872930579199_n_1UdxpkB.jpg",
        )
        fileObject.save()
        fileObject.file_topic.add(topicObject)

        folderObject = Folder(folder_name="testFolder")
        folderObject.save()

    def test_upload_url(self):
        upload_url = "/file/uploadfile"
        f = open(
            "FileManager/Data_for_tests/docs/120914674_1266836413655636_5862638872930579199_n_1UdxpkB.jpg",
            "rb",
        )
        f.read(4)
        data = {"folder": "testTopic", "topic": ["testTopic"], "file": [f]}
        response = self.client.post(upload_url, data)
        f.close()
        print(response)
        status_code = response.status_code
        self.assertEqual(status_code, 200)

    def test_upload_url_with_no_file(self):
        upload_url = "/file/uploadfile"
        data = {"folder": "testFolder", "topic": ["testTopic"], "file": []}
        response = self.client.post(upload_url, data)
        status_code = response.status_code
        self.assertEqual(status_code, 400)

    def test_same_file_exist_in_same_folder(self):
        upload_url = "/file/uploadfile"
        f = open(
            "FileManager/Data_for_tests/docs/120914674_1266836413655636_5862638872930579199_n_1UdxpkB.jpg",
            "rb",
        )
        f.read(4)
        data = {"folder": "testFolder", "topic": ["testTopic"], "file": [f, f]}
        response = self.client.post(upload_url, data)
        f.close()
        status_code = response.status_code
        self.assertEqual(status_code, 400)

    def test_new_topic_name(self):
        upload_url = "/file/uploadfile"
        f = open(
            "FileManager/Data_for_tests/docs/120914674_1266836413655636_5862638872930579199_n_1UdxpkB.jpg",
            "rb",
        )
        f.read(4)
        data = {"folder": "testFolder", "topic": ["newTestTopic"], "file": [f]}
        response = self.client.post(upload_url, data)
        f.close()
        status_code = response.status_code
        self.assertEqual(status_code, 200)

    def test_new_folder_name(self):
        upload_url = "/file/uploadfile"
        f = open(
            "FileManager/Data_for_tests/docs/120914674_1266836413655636_5862638872930579199_n_1UdxpkB.jpg",
            "rb",
        )
        f.read(4)
        data = {"folder": "newTestFolder", "topic": ["testTopic"], "file": [f]}
        response = self.client.post(upload_url, data)
        f.close()
        status_code = response.status_code
        self.assertEqual(status_code, 200)

    # TestCases for SEARCHING DOCUMENTS ----->

    def test_search_url(self):
        search_url = "/file/searchfile"
        data = '{"folder_name": "testFolder","topic": ["testTopic"],"file_name": ["testFile"]}'
        response = self.client.generic("POST", search_url, data)
        status_code = response.status_code
        self.assertEqual(status_code, 200)

    def test_folder_name_is_empty_and_no_topics_no_files(self):
        search_url = "/file/searchfile"
        data = '{"folder_name": "","topic": [],"file_name": []}'
        response = self.client.generic("POST", search_url, data)
        status_code = response.status_code
        self.assertEqual(status_code, 400)

    def test_no_file_found_of_given_topic(self):
        search_url = "/file/searchfile"
        data = '{"folder_name": "","topic": ["newTopic"],"file_name": []}'
        response = self.client.generic("POST", search_url, data)
        status_code = response.status_code
        self.assertEqual(status_code, 400)

    def test_file_found_for_given_topic(self):
        search_url = "/file/searchfile"
        data = '{"folder_name": "","topic": ["testTopic"],"file_name": []}'
        response = self.client.generic("POST", search_url, data)
        status_code = response.status_code
        self.assertEqual(status_code, 200)

    def test_found_file_by_folder_name_and_topics(self):
        search_url = "/file/searchfile"
        data = '{"folder_name": "testFolder","topic": ["testTopic"],"file_name": []}'
        response = self.client.generic("POST", search_url, data)
        status_code = response.status_code
        self.assertEqual(status_code, 200)

    def test_file_not_found_by_given_folder_and_topics(self):
        search_url = "/file/searchfile"
        data = '{"folder_name": "testFolder","topic": ["newTestTopic"],"file_name": []}'
        response = self.client.generic("POST", search_url, data)
        status_code = response.status_code
        self.assertEqual(status_code, 400)

    def test_find_file_by_only_folder_name(self):
        search_url = "/file/searchfile"
        data = '{"folder_name": "testFolder","topic": [],"file_name": []}'
        response = self.client.generic("POST", search_url, data)
        status_code = response.status_code
        self.assertEqual(status_code, 200)

    def test_folder_doesnt_exist(self):
        search_url = "/file/searchfile"
        data = '{"folder_name": "newTestFolder","topic": [],"file_name": []}'
        response = self.client.generic("POST", search_url, data)
        status_code = response.status_code
        self.assertEqual(status_code, 400)

    def test_only_topics_given(self):
        search_url = "/file/searchfile"
        data = '{"folder_name": "","topic": ["testTopic"],"file_name": []}'
        response = self.client.generic("POST", search_url, data)
        status_code = response.status_code
        self.assertEqual(status_code, 200)

    # test for delete...............................
    def test_delete_by_given_folder_name(self):
        delete_url = "/file/delete"
        data = '{"folder_name": "testFolder", "file_name": []}'
        response = self.client.generic("DELETE", delete_url, data)
        status_code = response.status_code
        self.assertEqual(status_code, 200)

    # def test_folder_doesnt_exist(self):
    #     delete_url = '/file/delete'
    #     data = '{"folder_name": "newTestFolder", "file_name": []}'
    #     response = self.client.generic('DELETE', delete_url, data)
    #     status_code = response.status_code
    #     self.assertEqual(status_code, 204)

    def test_delete_by_given_file_names(self):
        delete_url = "/file/delete"
        data = '{"folder_name": "", "file_name": ["testFile"]}'
        response = self.client.generic("DELETE", delete_url, data)
        status_code = response.status_code
        self.assertEqual(status_code, 200)

    def test_given_file_name_doesnt_exist(self):
        delete_url = "/file/delete"
        data = '{"folder_name": "", "file_name": ["newFileName"]}'
        response = self.client.generic("DELETE", delete_url, data)
        status_code = response.status_code
        self.assertEqual(status_code, 204)

    def test_folder_name_and_file_name_is_blank(self):
        delete_url = "/file/delete"
        data = '{"folder_name": "", "file_name": []}'
        response = self.client.generic("DELETE", delete_url, data)
        status_code = response.status_code
        self.assertEqual(status_code, 204)

    def test_delete_by_given_folder_name_and_file_name(self):
        delete_url = "/file/delete"
        data = '{"folder_name": "testFolder", "file_name": ["testFile"]}'
        response = self.client.generic("DELETE", delete_url, data)
        status_code = response.status_code
        self.assertEqual(status_code, 204)

    def test_folder_doesnt_exist_with_file_name_given(self):
        delete_url = "/file/delete"
        data = '{"folder_name": "newTestFolder", "file_name": ["testFile"]}'
        response = self.client.generic("DELETE", delete_url, data)
        status_code = response.status_code
        self.assertEqual(status_code, 204)
