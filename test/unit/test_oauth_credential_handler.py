import unittest
import os
from google.oauth2.credentials import Credentials
from source.google_auth.oauth_credential_handler import OAuthCredentialHandler


class TestOAuthCredentialHandler(unittest.TestCase):

    def setUp(self):
        oauth_credential_file = './token.json'
        self.new_oauth_credential_file = '.test_oauth_credential_file.json'
        self.oauth_credential_handler = OAuthCredentialHandler()
        self.oauth_credential_handler.set_oauth_credential_from_file(
            oauth_credential_file)

    def test_get_oauth_credential(self):
        self.assertIsInstance(
            self.oauth_credential_handler.get_oauth_credential(), Credentials)

    def test_is_valid(self):
        self.assertIsInstance(self.oauth_credential_handler.is_valid(), bool)

    def test_has_expired(self):
        self.assertIsInstance(
            self.oauth_credential_handler.has_expired(), bool)

    def test_write_oauth_credential_to_file(self):
        self.oauth_credential_handler.write_oauth_credential_to_file(
            self.new_oauth_credential_file)
        self.assertEqual(os.path.exists(self.new_oauth_credential_file), True)


if __name__ == '__main__':
    unittest.main()
