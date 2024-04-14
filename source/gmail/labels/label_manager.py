from source.gmail.labels.label_api import LabelAPI
import jmespath


class LabelManager:

    def __init__(self, userId, oauth_credentials):
        self.userId = userId
        self.labelAPI = LabelAPI(oauth_credentials)


    def create_label(self, name, messageList_visibility = None, label_list_visibility = None, background_color = None, text_color = None):
        
        label = {}

        label['name'] = name
        
        if messageList_visibility is not None:
            label['messageListVisibility'] = messageList_visibility
        if label_list_visibility is not None:
            label['labelListVisibility'] = label_list_visibility

        if background_color is not None or text_color is not None:
            label['color'] = {}
        
            if background_color is not None:
                label['color']['backgroundColor'] = background_color
            if text_color is not None:
                label['color']['textColor'] = text_color

        try:
            return self.labelAPI.create_label(userId = self.userId, label = label)
        except Exception as error:
            return error


    def get_label_by_id(self, label_id):
        try:
            return self.labelAPI.get_label(userId = self.userId, label_id = label_id)
        except Exception as error:
            return error


    def get_all_labels(self):
        try:
            return self.labelAPI.get_all_labels(userId = self.userId)
        except Exception as error:
            return error
        
    
    def get_labelId_by_name(self, name):

        try:
            labels = self.get_all_labels()
        except Exception as error:
            return error

        expression = jmespath.compile("labels[*].{id: id, name: name}")
        label_names_and_ids = expression.search(labels)

        for label_name_and_id in label_names_and_ids:
            if label_name_and_id['name'] == name:
                return label_name_and_id['id']


    def update_label_by_id(self, label_id, name = None, message_list_visibility = None, label_list_visibility = None, background_color = None, text_color = None):

        label = {}

        if name is not None:
            label['name'] = name
        if message_list_visibility is not None:
            label['messageListVisibility'] = message_list_visibility
        if label_list_visibility is not None:
            label['labelListVisibility'] = label_list_visibility
        
        if background_color is not None or text_color is not None:
            label['color'] = {}
        
            if background_color is not None:
                label['color']['backgroundColor'] = background_color
            if text_color is not None:
                label['color']['textColor'] = text_color
        try:
            return self.labelAPI.update_label(userId = self.userId, label_id = label_id, label = label)
        except Exception as error:
            return error


    def delete_label_by_id(self, label_id):
        try:
            self.labelAPI.delete_label(userId = self.userId, label_id = label_id)
        except Exception as error:
            return error


    def delete_all_labels(self):
        
        # Expression to get label user label ids
        expression = jmespath.compile("labels[?type=='user'].id")

        try:
            labels = self.get_all_labels()
        except Exception as error:
            return error
        
        # Run the expression against the labels to get a list of label Ids
        label_ids = expression.search(labels)
        
        if(len(label_ids) == 0):
            return None
        else:
            for label_id in label_ids:
                try:
                    self.delete_label_by_id(label_id = label_id)
                except Exception as error:
                    return error