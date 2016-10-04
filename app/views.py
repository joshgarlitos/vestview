from flask import render_template
from app import V_app

@V_app.route('/')
@V_app.route('/index')
def index():
	return render_template('index.html')
