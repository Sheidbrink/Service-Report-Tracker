from flask import Blueprint, render_template, session, url_for

index = Blueprint('index', __name__)

@index.route('/')
def home():
	return render_template('index.html', active='home')

@index.route('/help')
def help():
	return render_template('help.html', active='help')

@index.route('/contact')
def contact():
	return render_template('contactus.html', active='contact')