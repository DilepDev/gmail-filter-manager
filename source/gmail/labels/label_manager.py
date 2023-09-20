from source.gmail.labels.label_api import LabelAPI
import jmespath


class LabelManager:

    def __init__(self, userId, oauth_credentials):
        self.userId = userId
        self.labelAPI = LabelAPI(oauth_credentials)


    def create_label(self, name, messageListVisibility = None, labelListVisibility = None, backgroundColor = None, textColor = None):
        
        label = {}

        label['name'] = name
        
        if messageListVisibility is not None:
            label['messageListVisibility'] = messageListVisibility
        if labelListVisibility is not None:
            label['labelListVisibility'] = labelListVisibility

        if backgroundColor is not None or textColor is not None:
            label['color'] = {}
        
            if backgroundColor is not None:
                label['color']['backgroundColor'] = backgroundColor
            if textColor is not None:
                label['color']['textColor'] = textColor

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


    def update_label_by_id(self, label_id, name = None, messageListVisibility = None, labelListVisibility = None, backgroundColor = None, textColor = None):

        label = {}

        if name is not None:
            label['name'] = name
        if messageListVisibility is not None:
            label['messageListVisibility'] = messageListVisibility
        if labelListVisibility is not None:
            label['labelListVisibility'] = labelListVisibility
        
        if backgroundColor is not None or textColor is not None:
            label['color'] = {}
        
            if backgroundColor is not None:
                label['color']['backgroundColor'] = backgroundColor
            if textColor is not None:
                label['color']['textColor'] = textColor
        try:
            return self.labelAPI.update_label(userId = self.userId, label_id = label_id, label = label)
        except Exception as error:
            return error


    def delete_label_by_id(self, label_id):
        try:
            return self.labelAPI.delete_label(userId = self.userId, label_id = label_id)
        except Exception as error:
            return error


    def delete_all_labels(self):
        
        # Expression to get label ids of user label
        expression = jmespath.compile("labels[?type=='user'].{id: id, name: name}")

        try:
            labels = self.get_all_labels()
        except Exception as error:
            return error
        
        # Run the expression against the labels to get a list of label Ids
        label_names_and_ids = expression.search(labels)
        
        if(len(label_names_and_ids) == 0):
            return None
        else:
            print(f'Deleting {len(label_names_and_ids)} labels')

            for label_name_and_id in label_names_and_ids:
                try:
                    print(f"Deleting Label: {label_name_and_id}")
                    self.delete_label_by_id(label_id = label_name_and_id['id'])
                except Exception as error:
                    return error