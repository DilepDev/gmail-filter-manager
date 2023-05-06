"""Represents Gmail Service."""

from googleapiclient.discovery import build


class Gmail:
    """Represents Gmail Service."""

    def __init__(self):
        """Initialize Gmail Class."""
        self.gmail_service = None

    def set_gmail_service(self, oauth_credentials):
        """
        Build object to interact with gmail using the credentials.

        Arguments:
            credentials (google.oauth2.credentials.Credentials):
                The Credential object for authorization

        Raises:
            google.auth.exceptions.MutualTLSChannelError:
                If there are any problems setting up mutual TLS channel.

        Reference:
             https://googleapis.github.io/google-api-python-client/docs/epy/googleapiclient.discovery-module.html#build

        """
        self.gmail_service = build(
            'gmail', 'v1', credentials=oauth_credentials)

    def get_gmail_service(self):
        """
        Return a object to interact with gmail.

            Return:
                A Resource object with methods for interacting with the
                service.
        """
        return self.gmail_service

    def close(self):
        """Close httplib2 connections."""
        self.gmail_service.close()
