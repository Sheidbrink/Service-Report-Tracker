import views.document
from models.DBCommunicator import DBCommunicator

def search(formName, toSearch):
	dbCom = DBCommunicator.getInstance()
	return dbCom.find(formName, toSearch)

def submit(formName, toSubmit):
	dbCom = DBCommunicator.getInstance()
	dbCom.addDictionary(formName, toSubmit)
	return True

def loadDocument(formName):
	file = open('templates/reports.txt')
	partOfForm = False
	toReturn = []
	for line in file.readlines():
		if '\t' not in line:
			partOfForm = False
		if formName in line:
			partOfForm = True
			continue
		if partOfForm:
			line = line.replace('\t', '')
			line = line.replace('\n', '')
			pair = line.split(' : ')
			if len(pair) == 1:
				toReturn.append(pair[0])
			else:
				myTuple = pair[0], pair[1]
				toReturn.append(myTuple)
	return toReturn