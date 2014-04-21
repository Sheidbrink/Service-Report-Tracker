from flask import Flask, session, Blueprint, render_template, session, url_for, request, flash, redirect
from controller.controller import search, submit, loadDocument
import datetime
import json
document = Blueprint('document', __name__)

def getFormKeys(formName):
	allFields = loadDocument(formName)
	allkeys = []
	for field in allFields:
		if field is type(()):
			continue
		allkeys.append(field[1])
	return allkeys

def getSearchedValues(formName):
	toReturn = {}
	for field in getFormKeys(formName):
		toReturn[field] = session.get(field)
	return search(formName, toReturn)

@document.route('/create/<formName>')
def createDocument(formName):
	return render_template('documentPage.html', formName=formName, \
		allFields=loadDocument(formName), active='create', buttonName="Submit", \
		submitURL=url_for('document.submitdoc'))
	#return render_template('documentPage.html', active='bdocs', \
		#formName=formName, allFields=allFields, formValues=docValues, selected=selected)

@document.route('/submit', methods=['POST'])
def submitdoc():
	form = {}
	formName = request.form['formName']
	for key in request.form.keys():
		if 'formName' and 'Submit' not in key:
			form[key] = request.form[key]
	form['submittedOn'] = datetime.datetime.utcnow()
	successful = submit(formName, form)
	if successful:
		flash('Submitted Successfully')
		return redirect(url_for('document.createDocument', \
			formName=formName))
	else:
		flash('Error submitting')
		#perhaps keep values filled in here
		return redirect(url_for('document.createDocument', \
			formName=formName))#, docValues=form)

@document.route('/display/<formName><selectedIndex>', methods=['GET'])
def displaydoc(formName, selectedIndex):
	selectedIndex = int(selectedIndex)
	return render_template('search.html', formName=formName, \
		allFields=loadDocument(formName), active='search', \
		formValues=getSearchedValues(formName), selectedIndex=selectedIndex)

@document.route('/search/<formName>', methods=['POST', 'GET'])
def searchdocs(formName):
	if (request.method == 'GET'):
		return render_template('documentPage.html', formName=formName, \
			allFields=loadDocument(formName), active='search', buttonName="Search", \
			submitURL=url_for('document.searchdocs', formName=formName))
	elif (request.method == 'POST'):
		formName = request.form['formName']
		for key in request.form.keys():
			if 'formName' and 'Search' not in key:
				session[key] = request.form[key]
		matchedDict = getSearchedValues(formName)
		if(len(matchedDict) >= 1):
			return redirect(url_for('document.displaydoc', \
				formName=formName, selectedIndex=0))
		else:
			flash('Nothing Matching Search')
			return redirect(url_for('document.searchdocs', \
				formName=formName))
			

@document.route('/api', methods=['GET', 'POST'])
def api():
	if 'formName' not in request.headers:
		return 'No \'formName\' given'
	formName = request.headers['formName']
	allFormKeys = getFormKeys(formName)
	form = {}
	request.headers.keys()
	for key in request.headers.keys():
		if key in allFormKeys:
			form[key] = request.headers[key]
	if request.method == 'GET':
		matched = search(formName, form)
		toReturn = []
		for doc in matched:
			doc['submittedOn'] = str(doc['submittedOn'])
			del doc['_id']
			toReturn.append(doc)
		return json.dumps(toReturn)
	elif request.method == 'POST':
		form['submittedOn'] = datetime.datetime.utcnow()
		successful = submit(formName, form)
		if successful:
			return "Submitted Successfully"
		else:
			return "Submit Failed"