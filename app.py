from flask import Flask, redirect, session, url_for

app = Flask(__name__)

from views.index import index
app.register_blueprint(index)

from views.document import document
app.register_blueprint(document)

if __name__ == '__main__':
	app.secret_key = "idk what this is for, but had to use it to flash()"
	app.debug = True
	app.run(host='0.0.0.0')