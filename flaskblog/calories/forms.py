 
from flask_wtf import FlaskForm
from wtforms import  SubmitField, DateField, FloatField
from wtforms.validators import DataRequired 


class CalorieForm(FlaskForm):
    breakfast = FloatField('breakfast', validators=[DataRequired()])
    lunch = FloatField('lunch', validators=[DataRequired()])
    dinner= FloatField('dinner', validators=[DataRequired()])
    snacks = FloatField('snacks', validators=[DataRequired()])
    date_posted = DateField('Date Posted', validators=[DataRequired()])
    submit = SubmitField('Add')