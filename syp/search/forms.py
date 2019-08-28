from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class SearchRecipeForm(FlaskForm):
    recipe = StringField('Receta', validators=[DataRequired()])
    submit = SubmitField('Buscar')
