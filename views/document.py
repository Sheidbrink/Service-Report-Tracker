from flask import Flask, Blueprint, render_template, session, url_for, request

document = Blueprint('document', __name__)

@document.route('/browse')
def showdocs():
	return render_template('service_report.html', active='bdocs')

@document.route('/search', methods=['GET', 'POST'])
def searchdocs():
	if request.method == 'POST':
		if "search" in request.form:
			return "Search for something"
		elif "submit" in request.form:
			return "Submit Form" 
		return render_template('service_report.html', active='bdocs')