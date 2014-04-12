from flask import Flask, Blueprint, render_template, session, url_for, request, flash, redirect
from controller.Form import Form
document = Blueprint('document', __name__)


@document.route('/browse')
def dynamictest():
	allFields  = [ ("name 1", "value1"), \
					("name2" ,"value2") ]
	return render_template('documentPage.html', active='bdocs', allFields=allFields)

@document.route('/search', methods=['GET', 'POST'])
def searchdocs():
	if request.method == 'POST':
		if "search" in request.form:
			request = urllib2.Request("service_report.py")
			response = urllib2.urlopen(req)
			print req.read()

		elif "submit" in request.form:
			toSubmit = Form("FormTitle")
			for key in request.form.keys():
				if key == "submit":
					continue
				print "add:" + key +"value:" + request.form[key]
			flash('Submitted Successfully')
			return redirect(url_for('document.showdocs'))
		return render_template('documentPage.html', active='bdocs')

def loadDocument(name)
	file = open('../templates/reports.txt')