from source.gmail.filters.filter_api import FilterAPI
import jmespath
import json

class FilterManager:

    def __init__(self, userId, oauth_credentials):
        self.userId = userId
        self.filterAPI = FilterAPI(oauth_credentials)


    def set_criteria(self, from_address = None, to_address = None, subject = None, query = None, negated_query = None, size = None, size_comparison = None, has_attachement = False, exclude_chats = False):

        criteria = {}

        if from_address is not None:
            criteria['from'] = from_address
        if to_address is not None:
            criteria['to'] = to_address
        if subject is not None:
            criteria['subject'] = subject
        if query is not None:
            criteria['query'] = query
        if negated_query is not None:
            criteria['negatedQuery'] = negated_query
        if size is not None:
            criteria['size'] = size
        if size_comparison is not None:
            criteria['sizeComparison'] = size_comparison

        criteria['hasAttachment'] = has_attachement
        criteria['excludeChats'] = exclude_chats

        return criteria


    def create_filter(self, criteria, add_labels = [], remove_labels = [], forward = None):

        filter = {}
        filter['criteria'] = criteria

        if len(add_labels) > 0 or len(remove_labels) > 0 or len(remove_labels) > 0:
            
            filter['action'] = {}

            if len(add_labels) > 0:
                filter['action']['addLabelIds'] = add_labels
            if len(remove_labels) > 0:
                filter['action']['removeLabelIds'] = remove_labels
            if len(remove_labels) > 0:
                filter['action']['forward'] = forward

        return self.filterAPI.create_filter(userId = self.userId, filter = filter)


    def get_filter_by_id(self, filter_id):
        return self.filterAPI.get_filter(userId = self.userId, filter_id = filter_id)
    

    def get_all_filters(self):
        return self.filterAPI.get_all_filters(self.userId)
    

    def get_filterId_by_filter(self, filter):

        filters = self.filterAPI.get_all_filters(userId = self.userId)
        expression = jmespath.compile(f'filter[?criteria==`{json.dumps(filter['criteria'])}` && action==`{json.dumps(filter['action'])}`].id | [0]')
        filter_id = expression.search(filters)

        return filter_id


    def delete_filter_by_id(self, filter_id):
        self.filterAPI.delete_filter(self.userId, filter_id = filter_id)
    

    def delete_all_filters(self):
        
        filters = self.filterAPI.get_all_filters(userId = self.userId)
        expression = jmespath.compile(f'filter[*].id')
        filter_ids = expression.search(filters)

        if filter_ids is not None:
            for filter_id in filter_ids:
                self.filterAPI.delete_filter(self.userId, filter_id = filter_id)
