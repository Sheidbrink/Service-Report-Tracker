from flask import Flask, Blueprint, render_template, session, url_for, request, flash, redirect
from controller.controller import search, submit, loadDocument
document = Blueprint('document', __name__)


@document.route('/browse/<document>')
def renderDocument(document, docValues={}):
	allFields  = loadDocument(document)
	return render_template('documentPage.html', active='bdocs', \
		formName=document, allFields=allFields, formValues=docValues)

@document.route('/search', methods=['POST'])
def searchdocs():
	if(request.method == 'POST'):
		form = {}
		formName = request.form['formName']
		
		for key in request.form.keys():
			form[key] = request.form[key]
		del form['formName']
		#Search
		if "search" in request.form:
			del form['search']
			matchedDict = search(formName, form)
			if(len(matchedDict) >= 1):
				flash('Search Successful')
				return renderDocument(formName, matchedDict[0])
			else:
				flash('Invalid Search')
				return redirect(url_for('document.renderDocument', \
					document=formName))
		#Submit
		elif "submit" in request.form:
			del form['submit']
			successful = submit(formName, form)
			if successful:
				flash('Submitted Successfully')
				return redirect(url_for('document.renderDocument', \
					document=formName))
			else:
				flash('Error submitting')
		#Something Else
		flash('Unexpected Error')
		return renderDocument(document=formName, docValues=form)

@document.route('/api', methods=['GET', 'POST'])
def api():
	if request.method == 'GET':
		return search(request.form.copy())
	elif request.method == 'POST':
		return submit(request.form.copy())