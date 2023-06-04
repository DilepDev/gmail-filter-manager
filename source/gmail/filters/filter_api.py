from source.google_services.gmail import Gmail
from googleapiclient.errors import HttpError


class FilterAPI:

    def __init__(self, oauth_credentials):
        self.gmail = Gmail()
        self.gmail.set_gmail_service(oauth_credentials = oauth_credentials)
        self.gmail_filter_service = self.gmail.get_gmail_service().users().settings().filters()


    def get_filter(self, userId, filter_id):
        try:
            filter = self.gmail_filter_service.get(userId = userId, id = filter_id).execute()
            self.gmail.close()
            return filter
        except HttpError:
            return None
        except Exception as error:
            return error
    
    
    def create_filter(self, userId, filter):
        try:
            filter = self.gmail_filter_service.create(userId = userId, body = filter).execute()
            self.gmail.close()
            return filter
        except Exception as error:
            return error


    def get_all_filters(self, userId):
        try:
            filter = self.gmail_filter_service.list(userId = userId).execute()
            self.gmail.close()
            return filter
        except Exception as error:
            return error


    def delete_filter(self, userId, filter_id):
        try:
            filter = self.gmail_filter_service.delete(userId = userId, id = filter_id).execute()
            self.gmail.close()
            return filter
        except Exception as error:
            return error