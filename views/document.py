from flask import Flask, Blueprint, render_template, session, url_for, request, flash, redirect
from controller.controller import search, submit, loadDocument
import datetime
document = Blueprint('document', __name__)


@document.route('/create/<formName>')
def renderDocument(formName):
	allFields  = loadDocument(formName)
	return render_template('documentPage.html', active='bdocs', \
		formName=formName, allFields=allFields, formValues=docValues, selected=selected)

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
				cdate = matchedDict[0]['submittedOn']
				flash(str(cdate.date()) + ' ' + str(cdate.hour) + \
					':' + str(cdate.minute) + ':' + str(cdate.second) + ' - Search Successful')
				return renderDocument(formName, matchedDict, 0)
			else:
				flash('Nothing Matching Search')
				return redirect(url_for('document.renderDocument', \
					document=formName))
		#Submit
		elif "submit" in request.form:
			del form['submit']
			form['submittedOn'] = datetime.datetime.utcnow()
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