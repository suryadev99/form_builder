from flask_wtf import FlaskForm
from wtforms import (SubmitField, IntegerField,
                     FloatField, StringField,
                     TextAreaField, FormField, validators)
from flask_wtf.file import (FileField, FileRequired,
                            FileAllowed)

class Addform(FlaskForm):
    """
    Class for adding the final form
    """
    form_id = TextAreaField('form_id', [validators.DataRequired()])
    name = StringField('Name', [validators.DataRequired()])
    mobile_number = TextAreaField('Mobile_number', [validators.DataRequired()])
    gender = StringField('Gender', [validators.DataRequired()])
    email = TextAreaField('Email', [validators.DataRequired()])
    subject = TextAreaField('Subject', [validators.DataRequired()])

class add_unfilled_form(FlaskForm):
    """
    Class for adding the initial unfilled form
    """
    form_id = TextAreaField('form_id', [validators.DataRequired()])
    form_details = StringField('form_details', [validators.DataRequired()])
