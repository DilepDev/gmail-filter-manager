from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

from source.google_auth.authorization_handler import AuthorizationHandler


class OAuthCredentialHandler:

    def __init__(self):
        self.oauth_credential = None

    def generate_oauth_credential(self, client_secret, scopes):
        self.oauth_credential = AuthorizationHandler().authorize(
            client_secret, scopes)

    def set_oauth_credential_from_file(self, oauth_credential_file):
        self.oauth_credential = Credentials.from_authorized_user_file(
            oauth_credential_file)

    def get_oauth_credential(self):
        return self.oauth_credential

    def is_valid(self):
        return self.oauth_credential.valid

    def has_expired(self):
        return self.oauth_credential.expired

    def refresh_oauth_credential(self):
        self.oauth_credential.refresh(Request())

    def write_oauth_credential_to_file(self, oauth_credential_file,):
        with open(oauth_credential_file, 'w', encoding="utf-8") as oauth_credential:
            oauth_credential.write(self.oauth_credential.to_json())
