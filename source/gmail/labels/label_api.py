from source.google_services.gmail import Gmail
from googleapiclient.errors import HttpError


class LabelAPI:

    def __init__(self, oauth_credentials):
        self.gmail = Gmail()
        self.gmail.set_gmail_service(oauth_credentials = oauth_credentials)
        self.gmail_label_service = self.gmail.get_gmail_service().users().labels()


    def get_label(self, userId, label_id):
        try:
            label = self.gmail_label_service.get(userId = userId, id = label_id).execute()
            self.gmail.close()
            return label
        except HttpError:
            return None
        except Exception as error:
            print(type(error))
            return error
    
    
    def create_label(self, userId, label_dictionary):
        try:
            label = self.gmail_label_service.create(userId = userId, body = label_dictionary).execute()
            self.gmail.close()
            return label
        except Exception as error:
            return error


    def get_all_labels(self, userId):
        try:
            label = self.gmail_label_service.list(userId = userId).execute()
            self.gmail.close()
            return label
        except Exception as error:
            return error


    def update_label(self, userId, id, label_dictionary):
        try:
            label = self.gmail_label_service.update(userId = userId, id = id, body = label_dictionary).execute()
            self.gmail.close()
            return label
        except Exception as error:
            return error


    def delete_label(self, userId, label_id):
        try:
            label = self.gmail_label_service.delete(userId = userId, id = label_id).execute()
            self.gmail.close()
            return label
        except Exception as error:
            return error