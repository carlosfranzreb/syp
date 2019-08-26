from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class TimesForm(FlaskForm):
    time = StringField('Tiempo', validators=[DataRequired()])
    submit = SubmitField('Buscar')
