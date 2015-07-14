from flask.ext.wtf import Form
from wtforms import StringField
from wtforms.validators import DataRequired


class LinkForm(Form):
    link_one = StringField('link_one', validators=[DataRequired()])
    link_two = StringField('link_two', validators=[DataRequired()])
