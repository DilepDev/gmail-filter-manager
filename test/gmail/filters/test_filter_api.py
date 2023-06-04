import unittest
from source.gmail.filters.filter_api import FilterAPI
from source.google_auth.oauth_credential_handler import OAuthCredentialHandler


class TestFilterAPI(unittest.TestCase):

    def setUp(self):
        oauth_credential_file = './oauth_credential.json'
        self.oauth_credential_handler = OAuthCredentialHandler()
        self.oauth_credential_handler.set_oauth_credential_from_file(oauth_credential_file)
        self.filter_api = FilterAPI(self.oauth_credential_handler.get_oauth_credential())

    def tearDown(self):
        pass


class TestFilterAPIGet(TestFilterAPI):

    def setUp(self):
        super().setUp()
        self.filter = self.filter_api.create_filter('me', {'action': {'addLabelIds': ['STARRED']}, 'criteria' : {'to': 'test@test.com'}})

    def tearDown(self):
        self.filter_api.delete_filter('me', self.filter['id'])
        super().tearDown()

    def test_get_filter(self):
        self.assertEqual(self.filter_api.get_filter('me', self.filter['id'])['criteria']['to'], 'test@test.com')


class TestFilterAPICreate(TestFilterAPI):

    def setUp(self):
        super().setUp()
        self.filter = {'action': {'addLabelIds': ['STARRED']}, 'criteria' : {'to': 'test@test.com'}}

    def tearDown(self):
        self.filter_api.delete_filter('me', self.created_filter['id'])
        super().tearDown()

    def test_create_filter(self):
        self.created_filter = self.filter_api.create_filter('me', self.filter)
        self.assertEqual(self.created_filter['criteria']['to'], 'test@test.com')


class TestFilterAPIGetAll(TestFilterAPI):

    def setUp(self):
        super().setUp()
        filter = {'action': {'addLabelIds': ['STARRED']}, 'criteria' : {'to': 'test@test.com'}}
        self.created_filter = self.filter_api.create_filter('me', filter)

    def tearDown(self):
        super().tearDown()
        self.filter_api.delete_filter('me', self.created_filter['id'])

    def test_get_all_filters(self):
        all_filters = self.filter_api.get_all_filters('me')
        self.assertEqual('filter' in all_filters, True)


class TestFilterAPIDelete(TestFilterAPI):

    def setUp(self):
        super().setUp()
        filter = {'action': {'addLabelIds': ['STARRED']}, 'criteria' : {'to': 'test@test.com'}}
        self.created_filter = self.filter_api.create_filter('me', filter = filter)
    
    def tearDown(self):
        super().tearDown()

    def test_delete_filter(self):
        self.filter_api.delete_filter('me', filter_id = self.created_filter['id'])
        self.assertEqual(self.filter_api.get_filter('me', filter_id = self.created_filter['id']), None)
        


if __name__ == '__main__':
    unittest.main()