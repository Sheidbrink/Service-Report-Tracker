""" The form must have a "Name" key (i.e. Motor Service Report)"""

''' Form = {
                "Name" : name,
                "Form_attr" : attr, ...,
                "Category" : {
                                "Field" : value, ...,
                             }, ...,
            }
    i.e.
    Form = {
                "Name" : "Motor Service Report",
                "Work Performed for" : "Rocky Mtn Electric",
                "Date" : "10-2-2013",
                "Motor" : {
                                "Manufacturer" : "General Motor",
                                "Serial#" : "1234567890", ...,
                             }, ...,
            }'''

class Form(object):
    _info = {}
    '''Initialize the form with the name and any other form data''' 
    def __init__(self, name, **kwargs):
        self._info["Name"] = name
        for item in kwargs:
            self._info[item] = kwargs[item]

    '''Add category or form info'''
    def AddCategory(self, key, value=None):
        self._info[key] = value

    '''Add item to Category'''
    def AddItem(self, category, key, value=None):
        if category not in self._info:
            self._info[category] = {}
        if type(self._info[category]) is type(None):
            self._info[category] = {}
        if type(self._info[category]) is type({}):
            self._info[category][key] = value
            return True
        return False

    def GetValue(self, key, keyTwo=None):
        if key in self._info:
            if keyTwo is not type(None) and keyTwo in self._info[key]:
                return self._info[key][keyTwo]
            return self._info[key]
        return None

    def GetRootKeys(self):
        return self._info.keys()

    def GetInfo(self):
        return self._info
