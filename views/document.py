from flask import Flask, Blueprint, render_template, session, url_for, request, flash, redirect
from controller.controller import search, submit, loadDocument
import datetime
document = Blueprint('document', __name__)


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
		#Search
		del form['search']
		matchedDict = search(formName, form)
		if(len(matchedDict) >= 1):
			cdate = matchedDict[0]['submittedOn']
			flash(str(cdate.date()) + ' ' + str(cdate.hour) + \
				':' + str(cdate.minute) + ':' + str(cdate.second) + ' - Search Successful')
			return createDocument(formName, matchedDict, 0)
		else:
			flash('Nothing Matching Search')
			return redirect(url_for('document.createDocument', \
				document=formName))
			

@document.route('/api', methods=['GET', 'POST'])
def api():
	if request.method == 'GET':
		return search(request.form.copy())
	elif request.method == 'POST':
		return submit(request.form.copy())