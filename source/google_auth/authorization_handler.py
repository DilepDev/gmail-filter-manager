"""Authorize Google Services.

Usage example:

  foo = AuthorizationHandler()
  bar = foo.authorize(client_secret_file, authorization_scopes, port=0)
"""
from google_auth_oauthlib.flow import InstalledAppFlow


class AuthorizationHandler:
    """Handles Google Authorization Flow."""

    def authorize(self, client_secret_file, authorization_scopes, port=0):
        """
        Authorize User for the provided scopes using google InstalledAppFlow.

        Authenticates User and Authorizes User to use the scopes provided.

        Arguments:
            client_secret_file (str):
                Location of the client_secret.json file.
            authorization_scopes (Sequence[str]):
                The list of scopes to request during the flow
            port (int):
                The port for the local redirect server.
                default is 0

        Returns:
            google.oauth2.credentials.Credentials.

            A google Credential Object containing Oauth 2.0
            credentials for the user.

        Raises:
            No Exceptions are raised.
        """
        flow = InstalledAppFlow.from_client_secrets_file(client_secret_file, authorization_scopes)
        oauth_credentials = flow.run_local_server(port=port)
        return oauth_credentials
