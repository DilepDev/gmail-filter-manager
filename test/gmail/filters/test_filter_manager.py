import unittest
from source.gmail.filters.filter_manager import FilterManager
from source.google_auth.oauth_credential_handler import OAuthCredentialHandler


class TestFilterManager(unittest.TestCase):

    def setUp(self):
        oauth_credential_file = './oauth_credential.json'
        self.oauth_credential_handler = OAuthCredentialHandler()
        self.oauth_credential_handler.set_oauth_credential_from_file(oauth_credential_file)
        self.filter_manager = FilterManager(userId = 'me', oauth_credentials = self.oauth_credential_handler.get_oauth_credential())
        
        self.filter_manager.delete_all_filters()
        self.filter_manager.set_criteria()
        
        self.from_address = 'from@test.com'
        self.to_address = 'to@test.com'
        self.subject = 'test_subject'
        self.query = '"google"'
        self.negated_query = 'holiday AROUND 10 vacation'
        self.size = 1000
        self.size_comparison = "larger" 
        self.has_attachement = True
        self.exclude_chats = True

    def tearDown(self):
        self.filter_manager.delete_all_filters()


class TestFilterManagerCriteria(TestFilterManager):

    def setUp(self):
        super().setUp()

    def tearDown(self):
        super().tearDown()
        
    def test_set_criteria(self):
        criteria = self.filter_manager.set_criteria(from_address = self.from_address, to_address = self.to_address, subject = self.subject, query = self.query, negated_query = self.negated_query, size = self.size, size_comparison = self.size_comparison, has_attachement = self.has_attachement, exclude_chats = self.exclude_chats)
        self.assertEqual(criteria['from'], self.from_address)
        self.assertEqual(criteria['to'], self.to_address)
        self.assertEqual(criteria['subject'], self.subject)
        self.assertEqual(criteria['query'], self.query)
        self.assertEqual(criteria['negatedQuery'], self.negated_query)
        self.assertEqual(criteria['size'], self.size)
        self.assertEqual(criteria['sizeComparison'], self.size_comparison)
        self.assertEqual(criteria['hasAttachment'], self.has_attachement)
        self.assertEqual(criteria['excludeChats'], self.exclude_chats)


class TestFilterManagerCreate(TestFilterManager):

    def setUp(self):
        super().setUp()
        self.criteria = self.filter_manager.set_criteria(subject = self.subject, query = self.query, negated_query = self.negated_query, size = self.size, size_comparison = self.size_comparison)

    def tearDown(self):
        super().tearDown()
        
    def test_create_filter(self):
        
        add_labels = ["STARRED"]
        remove_labels = ["INBOX"]
        created_filter = self.filter_manager.create_filter(criteria = self.criteria, add_labels = add_labels, remove_labels = remove_labels)
        
        # Remove Defaults returned by filterAPI
        self.criteria.pop('hasAttachment')
        self.criteria.pop('excludeChats')

        self.assertDictEqual(created_filter['criteria'], self.criteria)
        self.assertEqual(created_filter['action']['addLabelIds'], add_labels)
        self.assertEqual(created_filter['action']['removeLabelIds'], remove_labels)
        

class TestFilterManagerGetById(TestFilterManager):

    def setUp(self):
        super().setUp()
        add_labels = ["STARRED"]
        remove_labels = ["INBOX"]
        self.criteria = self.filter_manager.set_criteria(from_address = self.from_address, has_attachement = self.has_attachement, exclude_chats = self.exclude_chats)
        self.created_filter = self.filter_manager.create_filter(criteria = self.criteria, add_labels = add_labels, remove_labels = remove_labels)

    def tearDown(self):
        super().tearDown()

    def test_get_filter_by_Id(self):
        self.assertEqual(self.filter_manager.get_filter_by_id(self.created_filter['id'])['criteria']['from'], self.criteria['from'])


class TestFilterManagerGetAll(TestFilterManager):

    def setUp(self):
        super().setUp()
        add_labels = ["STARRED"]
        remove_labels = ["INBOX"]
        self.criteria = self.filter_manager.set_criteria(from_address = self.from_address, has_attachement = self.has_attachement, exclude_chats = self.exclude_chats)
        self.created_filter = self.filter_manager.create_filter(criteria = self.criteria, add_labels = add_labels, remove_labels = remove_labels)


    def tearDown(self):
        super().tearDown()
        
    def test_get_all_filters(self):
        all_filters = self.filter_manager.get_all_filters()
        self.assertEqual('filter' in all_filters, True)


class TestFilterManagerGetIdByFilter(TestFilterManager):

    def setUp(self):
        super().setUp()
        self.add_labels = ["STARRED"]
        self.remove_labels = ["INBOX"]
        self.criteria = self.filter_manager.set_criteria(from_address = self.from_address, has_attachement = self.has_attachement, exclude_chats = self.exclude_chats)
        self.created_filter = self.filter_manager.create_filter(criteria = self.criteria, add_labels = self.add_labels, remove_labels = self.remove_labels)

    def tearDown(self):
        super().tearDown()

    def test_get_filterId_by_filter(self):
        self.assertEqual(self.filter_manager.get_filterId_by_filter({'criteria': self.criteria, 'action': {'addLabelIds': self.add_labels, 'removeLabelIds': self.remove_labels}}), self.created_filter['id'])


class TestFilterManagerDelete(TestFilterManager):

    def setUp(self):
        super().setUp()
        add_labels = ["STARRED"]
        remove_labels = ["INBOX"]
        self.criteria = self.filter_manager.set_criteria(from_address = self.from_address, to_address = self.to_address, subject = self.subject, query = self.query, negated_query = self.negated_query, size = self.size, size_comparison = self.size_comparison, has_attachement = self.has_attachement, exclude_chats = self.exclude_chats)
        self.created_filter = self.filter_manager.create_filter(criteria = self.criteria, add_labels = add_labels, remove_labels = remove_labels)

    def tearDown(self):
        super().tearDown()
        
    def test_delete_filter_by_id(self):
        self.assertEqual(self.filter_manager.delete_filter_by_id(filter_id = self.created_filter['id']), None)


class TestFilterManagerDeleteAll(TestFilterManager):

    def setUp(self):
        super().setUp()
        add_labels = ["STARRED"]
        remove_labels = ["INBOX"]
        self.criteria = self.filter_manager.set_criteria(from_address = self.from_address, to_address = self.to_address, subject = self.subject, query = self.query, negated_query = self.negated_query, size = self.size, size_comparison = self.size_comparison, has_attachement = self.has_attachement, exclude_chats = self.exclude_chats)
        self.created_filter = self.filter_manager.create_filter(criteria = self.criteria, add_labels = add_labels, remove_labels = remove_labels)

    def tearDown(self):
        super().tearDown()

    def test_delete_all_filters(self):
        self.assertEqual(self.filter_manager.delete_all_filters(), None)


if __name__ == '__main__':
    unittest.main()
