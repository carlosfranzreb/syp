from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class RecipesForm(FlaskForm):
    recipe = StringField('Receta', validators=[DataRequired()])
    submit = SubmitField('Buscar')
