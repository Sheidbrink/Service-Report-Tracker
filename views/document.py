from flask import Flask, Blueprint, render_template, session, url_for, request, flash, redirect
from controller.controller import search, submit, loadDocument
import datetime
import json
document = Blueprint('document', __name__)

searchedValues = []

@document.route('/create/<formName>')
def createDocument(formName):
	allFields  = loadDocument(formName)
	return render_template('documentPage.html', formName=formName, \
		allFields=allFields, active='create', buttonName="Submit", \
		submitURL=url_for('document.submitdoc'))
	#return render_template('documentPage.html', active='bdocs', \
		#formName=formName, allFields=allFields, formValues=docValues, selected=selected)

@document.route('/submit', methods=['POST'])
def submitdoc():
	form = {}
	formName = request.form['formName']
	for key in request.form.keys():
		form[key] = request.form[key]
	del form['formName']
	del form['Submit']
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
	allFields = loadDocument(formName)
	return render_template('search.html', formName=formName, \
		allFields=allFields, active='search', formValues=searchedValues, \
		selectedIndex=selectedIndex)

@document.route('/search/<formName>', methods=['POST', 'GET'])
def searchdocs(formName):
	if (request.method == 'GET'):
		allFields = loadDocument(formName)
		return render_template('documentPage.html', formName=formName, \
			allFields=allFields, active='search', buttonName="Search", \
			submitURL=url_for('document.searchdocs', formName=formName))
	elif (request.method == 'POST'):
		form = {}
		formName = request.form['formName']
		for key in request.form.keys():
			form[key] = request.form[key]
		del form['formName']
		del form['Search']
		matchedDict = search(formName, form)
		global searchedValues
		searchedValues = matchedDict
		if(len(matchedDict) >= 1):
			allFields = loadDocument(formName)
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
	allFields = loadDocument(formName)
	form = {}
	request.headers.keys()
	for key in request.headers.keys():
		if key in allFields:
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