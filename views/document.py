from flask import Flask, Blueprint, render_template, session, url_for, request, flash, redirect
from controller.Form import Form
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
			toSubmit = Form("FormTitle")
			for key in request.form.keys():
				if key == "submit":
					continue
				print "add:" + key +"value:" + request.form[key]
			flash('Submitted Successfully')
			return redirect(url_for('document.showdocs'))
		return render_template('service_report.html', active='bdocs')