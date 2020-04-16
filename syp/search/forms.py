from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class SearchRecipeForm(FlaskForm):
    """Used in search/recipe.html, to search for a recipe name,
    no matter the cook. Also used in search/cook_recipes.html,
    where the username is set outside the form. """
    recipe = StringField('Receta', validators=[DataRequired()])
    submit = SubmitField('Buscar')
