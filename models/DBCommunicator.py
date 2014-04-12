from pymongo import MongoClient
from controller.Form import Form

''' Each collection is a collection of Forms
    Perhaps each database is user or company '''

class DBCommunicator(object):
    # select where to connect to the database and the database to connect to
    # Perhaps have each user who logs in as a different database?
    def __init__(self, dbname, hostname='localhost', port=27017):
        self.client = MongoClient(hostname, port)
        self.db = client[dbname]

    def addDictionary(self, formName, myDict)
        if type(myDict) is type({}):
            collectionName = formName
            collection = self.db[collectionName]
            collection.insert(myDict)

    def find(self, formName, myDict)
        collectionName = formName
        collection = self.db[collectionName]
        toReturn = []
        for item in collection.find(myDict):
            toReturn.append(item)
        return toReturn





'''
    def AddForm(self, form)

        if type(form) is Form.Form:
            collection = self.db[form['Name'].replace(' ','-')]
            collection.insert(form)
            return True
        else:
            return False

    def Find(self, search, formName)
        formName = formName.replace(' ','-')
        if type(search) is type({}):
            collection = self.db[formName]
            forms = []
            for form in collection.find(search):
                forms.append(form)
            return forms
        return []

    def GetAllForms(self, formName)
        formName = formName.replace(' ','-')
        collection = self.db[formName]
        return collection.find()
'''