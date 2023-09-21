import unittest
from source.gmail.labels.label_manager import LabelManager
from source.google_auth.oauth_credential_handler import OAuthCredentialHandler


class TestLabelManager(unittest.TestCase):

    def setUp(self):
        oauth_credential_file = './oauth_credential.json'
        self.oauth_credential_handler = OAuthCredentialHandler()
        self.oauth_credential_handler.set_oauth_credential_from_file(oauth_credential_file)
        self.label_manager = LabelManager(userId = 'me', oauth_credentials = self.oauth_credential_handler.get_oauth_credential())
        
        self.label_manager.delete_all_labels()
        
        self.name = 'test_label'
        self.messageListVisibility = 'show'
        self.labelListVisibility = 'labelHide'
        self.backgroundColor = '#efefef'
        self.textColor = '#fad165'

    def tearDown(self):
        self.label_manager.delete_all_labels()


class TestLabelManagerCreate(TestLabelManager):

    def setUp(self):
        super().setUp()

    def tearDown(self):
        super().tearDown()
        
    def test_create_label(self):
        self.created_label = self.label_manager.create_label(name = self.name, messageListVisibility = self.messageListVisibility, labelListVisibility = self.labelListVisibility, backgroundColor = self.backgroundColor, textColor = self.textColor)
        self.assertEqual(self.created_label['name'], self.name)
        self.assertEqual(self.created_label['messageListVisibility'], self.messageListVisibility)
        self.assertEqual(self.created_label['labelListVisibility'], self.labelListVisibility)
        self.assertEqual(self.created_label['color']['backgroundColor'], self.backgroundColor)
        self.assertEqual(self.created_label['color']['textColor'], self.textColor)


class TestLabelManagerGetById(TestLabelManager):

    def setUp(self):
        super().setUp()
        self.created_label = self.label_manager.create_label(name = self.name, messageListVisibility = self.messageListVisibility, labelListVisibility = self.labelListVisibility, backgroundColor = self.backgroundColor, textColor = self.textColor)

    def tearDown(self):
        super().tearDown()

    def test_get_label_by_Id(self):
        self.assertEqual(self.label_manager.get_label_by_id(self.created_label['id'])['name'], self.name)
        self.assertEqual(self.label_manager.get_label_by_id(self.created_label['id'])['messageListVisibility'], self.messageListVisibility)
        self.assertEqual(self.label_manager.get_label_by_id(self.created_label['id'])['labelListVisibility'], self.labelListVisibility)
        self.assertEqual(self.label_manager.get_label_by_id(self.created_label['id'])['color']['backgroundColor'], self.backgroundColor)
        self.assertEqual(self.label_manager.get_label_by_id(self.created_label['id'])['color']['textColor'], self.textColor)


class TestLabelManagerGetAll(TestLabelManager):

    def setUp(self):
        super().setUp()

    def tearDown(self):
        super().tearDown()
        
    def test_get_all_labels(self):
        all_labels = self.label_manager.get_all_labels()
        self.assertEqual('labels' in all_labels, True)


class TestLabelManagerGetIdByName(TestLabelManager):

    def setUp(self):
        super().setUp()
        self.created_label = self.label_manager.create_label(name = self.name)

    def tearDown(self):
        super().tearDown()

    def test_get_labelId_by_name(self):
        self.assertEqual(self.label_manager.get_labelId_by_name(self.name),  self.created_label['id'])


class TestLabelManagerUpdateById(TestLabelManager):

    def setUp(self):
        super().setUp()
        self.created_label = self.label_manager.create_label(name = self.name, messageListVisibility = self.messageListVisibility, labelListVisibility = self.labelListVisibility, backgroundColor = self.backgroundColor, textColor = self.textColor)
        self.updated_label = {'name': 'updated_label'}

    def tearDown(self):
        super().tearDown()
        
    def test_update_label_by_id(self):
        self.assertEqual(self.label_manager.update_label_by_id(label_id = self.created_label['id'], name = self.updated_label['name'])['name'], self.updated_label['name'])


class TestLabelManagerDelete(TestLabelManager):

    def setUp(self):
        super().setUp()
        self.created_label = self.label_manager.create_label(name = self.name, messageListVisibility = self.messageListVisibility, labelListVisibility = self.labelListVisibility, backgroundColor = self.backgroundColor, textColor = self.textColor)

    def tearDown(self):
        super().tearDown()
        
    def test_delete_label(self):
        self.label_manager.delete_label_by_id(label_id = self.created_label['id'])
        self.assertEqual(self.label_manager.get_label_by_id(label_id = self.created_label['id']), None)


if __name__ == '__main__':
    unittest.main()
