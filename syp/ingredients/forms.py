from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length


class IngredientsForm(FlaskForm):
    """ Used to search recipes by ingredient. """
    ingredient = StringField('Ingrediente', validators=[DataRequired()])
    submit = SubmitField('Buscar')


class IngredientForm(FlaskForm):
    """ Used to edit and create new ingredients. """
    name = StringField('Nombre', validators=[DataRequired(), Length(max=50)])
    health = TextAreaField('Comentario', validators=[DataRequired()])
    save = SubmitField('Guardar')
