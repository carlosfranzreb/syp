from flask import Blueprint, render_template
from syp.search.forms import RecipesForm
from syp.recipes.utils import get_last_recipes


errors = Blueprint('errors', __name__)


@errors.app_errorhandler(404)
def error_404(error):
    return render_template('errors/404.html',
                           title='404',
                           recipe_form=RecipesForm(),
                           last_recipes=get_last_recipes(4)), 404


@errors.app_errorhandler(500)
def error_500(error):
    return render_template('errors/500.html',
                           title='500',
                           recipe_form=RecipesForm(),
                           last_recipes=get_last_recipes(4)), 500
