#!/usr/bin/env python

from flask import Flask, flash, request, Response, render_template, session, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc
from config import config, APP_IS_SUCCESS, logger
from formbuilder import formLoader
import json
import uuid
from models import *
from form import Addform, add_unfilled_form

app = Flask(__name__, static_folder='src')

app.secret_key = 'Sh3r1n4Mun4F'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///myforms.db'

db = SQLAlchemy(app)

cart={}

@app.route('/')
def index():
	"""
    Home page for form builder
    """
	return render_template('index.html', base_url=config['base_url'])

@app.route('/save', methods=['POST'])
def save():
	"""
    Function for saving the created form
    """
	try:
		response = {APP_IS_SUCCESS:False}
		add = add_unfilled_form()
		if request.method == 'POST':
			formData = json.loads(request.form.get('formData'))
			form_id = str(uuid.uuid4())
			add_product = initial_forms(
				form_id=form_id, form_details=json.dumps(formData)
			)
			db.session.add(add_product)
			db.session.commit()
			response["form_id"] = form_id
			if formData == 'None':
				return 'Error processing request'

			session['form_data'] = json.dumps(formData)
	except Exception as ex:
		msg = f"Exception occured in save handler route: - {ex}"
		logger.exception(msg)
		response["msg"] = msg

	return response

@app.route("/render/<form_id2>/",methods=["POST","GET"])
def render(form_id2):
	"""
    Function for rendering the created form
    """
	try:
		if not session['form_data']:
			form= one_form_by_id(form_id2)
			data = form.form_details
			session['form_data'] = data
			if not form: 
				return redirect('/')
			else:
				form_data = data
		else:
			form_data = session['form_data']
			session['form_data'] = None

		form_loader = formLoader(form_data, '{0}/submit/{1}/'.format(config['base_url'], form_id2))
		render_form = form_loader.render_form()
	
	except Exception as ex:
		msg = f"Exception occured in render handler route: - {ex}"
		logger.exception(msg)
		response["msg"] = msg
	return render_template('render.html', render_form=render_form)

@app.route("/edit/<form_id2>/",methods=["POST","GET"])
def edit(form_id2):
	"""
    Function for editing the form
    """
	form= final_form_by_id(form_id2)
	if not form: 
		return redirect('/')
	return render_template('edit.html', form=form)

@app.route("/List",methods=["POST","GET"])
def list_forms():
	"""
    Function for listing all the form
    """
	prods= forms_fill()
	return render_template("allforms.html",prod=prods,l=len(prods))


@app.route("/view/<form_id2>/",methods=["POST","GET"])
def view(form_id2):
	"""
    Function for viewing the form
    """
	form= final_form_by_id(form_id2)
	if not form: 
		return render_error_page(error_message = "Please Submit the form first")

	return render_template('view.html', render_form=form)

@app.route('/submit/<form_id2>/', methods=['POST'])
def submit(form_id2):
	"""
    Function for submitting the form
    """
	response = {APP_IS_SUCCESS: False}
	try:
		sub = []
		choice_len = 0
		form = Addform()
		info = one_form_by_id(form_id2)
		data = json.loads(info.form_details)
		for i in range(len(data["fields"])) :
			if data["fields"][i]["title"] == "subject":
				choice_len = len(data["fields"][i]["choices"])

		if request.method == 'POST':
			jsonData = request.get_json()
			value = request.form
			for i in range(choice_len):
				if f"subject_{i}" in value:
					sub.append(value[f"subject_{i}"])
			form_id = info.form_id
			name = form.name.data
			mobile_number = form.mobile_number.data
			email = form.email.data
			gender = form.gender.data
			subject = str(jsonData["subject"])
			add_product = Forms(
				form_id=form_id,
				name=name, 
				mobile_number=mobile_number,
				email=email,
				gender=gender,
				subject=subject
			)
			form = final_form_by_id(form_id2)
			if form:
				db.session.merge(add_product)
				db.session.commit()
			db.session.add(add_product)
			response["msg"] = (f"{name} is added to the db successfully!!!")
			response[APP_IS_SUCCESS] = True 
			db.session.commit()
	except exc.IntegrityError:
		db.session.rollback()
		db.session.flush()
		db.session.commit()
	except Exception as ex:
		msg = f"Exception occured in submit handler route: {form_id2} - {ex}"
		logger.exception(msg)
		response["msg"] = msg
		raise ex

	return response

@app.route('/search',methods=['GET', 'POST'])
def search():
	"""
    Function for searching the form
    """
	try:
		name=request.form['s']
		search = "%{}%".format(name)
		prdt=form_search_query(search)
		print(prdt)
	except Exception as ex:
		msg = f"Exception occured in search handler route- {ex}"
		logger.exception(msg)
		raise(ex)
	return render_template('allforms.html', prod=prdt,l=len(prdt))

@app.route('/delete/<form_id2>/',methods=['GET', 'POST'])
def delete(form_id2):
	"""
    Function for deleting the form
    """
	response = {APP_IS_SUCCESS: False}
	try:
		form_delete(form_id2)
		response[APP_IS_SUCCESS] = True
	except Exception as ex:
		msg = f"Exception occured in delete handler route: {form_id2} - {ex}"
		response["msg"] = msg
		logger.exception(msg)
		raise(ex)
	return redirect('/List')

def render_error_page(error_message, error_code=500):
    """
    Function for rendering error page
    """
    return render_template(
        "error.html",
        error_code=error_code,
        error_message=error_message,
    )

if __name__ == '__main__':
	app.debug = True
	app.run(host='0.0.0.0', port=5000)
