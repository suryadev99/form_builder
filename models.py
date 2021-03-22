from index import db
from sqlalchemy import or_

class Forms(db.Model):
    """
    Class for submitting the final form
    """
    form_id = db.Column(db.Text, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    #Taking mobile number as text since sqlite cannot store the large number as integer
    mobile_number = db.Column(db.Text, default=0)
    email = db.Column(db.Text, nullable=False)
    gender = db.Column(db.String(80))
    subject = db.Column(db.Text, nullable=False)


class initial_forms(db.Model):
    """
    Class for storing initially created form
    """
    form_id = db.Column(db.Text, primary_key=True)
    form_details = db.Column(db.String(80), nullable=False)


def all_forms():
    return Forms.query.order_by(Forms.form_id).all()

def final_form_by_id(id):
    return db.session.query(Forms).filter_by(form_id=id).first()

def one_form_by_id(id):
    return db.session.query(initial_forms).filter_by(form_id=id).first()

def forms_fill():
    return initial_forms.query.order_by(initial_forms.form_id).all()

def form_search_query(sr):
    return db.session.query(initial_forms).filter(or_(initial_forms.form_id.like(sr),initial_forms.form_id.like(sr))).all()

def form_delete(id):
    db.session.query(initial_forms).filter_by(form_id=id).delete()
    db.session.commit()


db.create_all()