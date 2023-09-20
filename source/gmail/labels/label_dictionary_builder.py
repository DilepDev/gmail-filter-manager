class LabelDictionaryBuilder:

    def __init__(self):
        self.label_dictionary = {}

    def setName(self, name):
        self.label_dictionary['name'] = name

    def setmessageListVisibility(self, messageListVisibility):
        self.label_dictionary['messageListVisibility'] = messageListVisibility

    def setLabelListVisibility(self, labelListVisibility):
        self.label_dictionary['labelListVisibility'] = labelListVisibility

    def setColor(self):
        if 'color' in self.label_dictionary:
            pass
        else:
            self.label_dictionary['color'] = {}

    def setBackgroundColor(self, backgroundColor):
        self.setColor()
        self.label_dictionary['color']['backgroundColor'] = backgroundColor

    def setTextColor(self, textColor):
        self.setColor()
        self.label_dictionary['color']['textColor'] = textColor

    def getLabelDictionary(self):
        return self.label_dictionary