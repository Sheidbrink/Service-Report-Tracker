from flask import Flask, Blueprint, render_template, session, url_for, request, flash, redirect
from controller.Form import Form
import urllib2
document = Blueprint('document', __name__)


@document.route('/browse')
def dynamictest():
	allFields  = [ ("name 1", "value1"), \
					("name2" ,"value2") ]
	return render_template('documentPage.html', active='bdocs', allFields=allFields)

@document.route('/search', methods=['GET', 'POST'])
def searchdocs():
	if(request.method == 'POST'):
		if "search" in request.form:
			return search()

		elif "submit" in request.form:
			return submit()

	return render_template('service_report.html', active='bdocs')

@document.route('/api', methods=['GET', 'POST'])
def api():
	if request.method == 'GET':
		return search()
	elif request.method == 'POST':
		return submit()

def search():
	return "Searching..."

def submit():
	toSubmit = Form("FormTitle")
	for key in request.form.keys():
		if key == "submit":
			continue
		print "add:" + key +"value:" + request.form[key]
	flash('Submitted Successfully')
	return redirect(url_for('document.showdocs'))
def loadDocument(name)
	file = open('../templates/reports.txt')
