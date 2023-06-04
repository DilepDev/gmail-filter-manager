import unittest
from source.gmail.labels.label_api import LabelAPI
from source.google_auth.oauth_credential_handler import OAuthCredentialHandler


class TestLabelAPI(unittest.TestCase):

    def setUp(self):
        oauth_credential_file = './oauth_credential.json'
        self.oauth_credential_handler = OAuthCredentialHandler()
        self.oauth_credential_handler.set_oauth_credential_from_file(oauth_credential_file)
        self.label_api = LabelAPI(self.oauth_credential_handler.get_oauth_credential())

    def tearDown(self):
        pass


class TestLabelAPIGet(TestLabelAPI):

    def setUp(self):
        super().setUp()

    def tearDown(self):
        super().tearDown()

    def test_get_label(self):
        self.assertEqual(self.label_api.get_label(userId = 'me', label_id = 'CHAT')['name'], 'CHAT')


class TestLabelAPICreate(TestLabelAPI):

    def setUp(self):
        super().setUp()
        self.label = {'name': 'test_run'}

    def tearDown(self):
        self.label_api.delete_label(userId = 'me', label_id = self.created_label['id'])
        super().tearDown()
        
    def test_create_label(self):
        self.created_label = self.label_api.create_label(userId = 'me', label = self.label)
        self.assertEqual(self.created_label['name'], self.label['name'])


class TestLabelAPIGetAll(TestLabelAPI):

    def setUp(self):
        super().setUp()

    def tearDown(self):
        super().tearDown()
        
    def test_get_all_labels(self):
        all_labels = self.label_api.get_all_labels(userId = 'me')
        self.assertEqual('labels' in all_labels, True)


class TestLabelAPIUpdate(TestLabelAPI):

    def setUp(self):
        super().setUp()
        self.label = {'name': 'new_label'}
        self.updated_label = {'name': 'updated_label'}
        self.created_label = self.label_api.create_label(userId = 'me', label = self.label)

    def tearDown(self):
        self.label_api.delete_label(userId = 'me', label_id = self.created_label['id'])
        super().tearDown()
        
    def test_update_label(self):
        self.assertEqual(self.label_api.update_label(userId = 'me', label_id = self.created_label['id'], label = self.updated_label)['name'], self.updated_label['name'])


class TestLabelAPIDelete(TestLabelAPI):

    def setUp(self):
        super().setUp()
        label = {'name': 'new_label'}
        self.created_label = self.label_api.create_label(userId = 'me', label = label)

    def tearDown(self):
        super().tearDown()
        
    def test_delete_label(self):
        self.label_api.delete_label(userId = 'me', label_id = self.created_label['id'])
        self.assertEqual(self.label_api.get_label(userId = 'me', label_id = self.created_label['id']), None)


if __name__ == '__main__':
    unittest.main()
