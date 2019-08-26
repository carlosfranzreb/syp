from flask import Blueprint, render_template
from syp.recipes.utils import get_recipe_by_name, get_last_recipes, \
                              get_recipe_keywords, get_real_name
from syp.search.forms import RecipesForm


recipes = Blueprint('recipes', __name__)


@recipes.route('/receta/<recipe_name>',
               methods=['GET', 'POST'])
def get_recipe(recipe_name):
    real_name = get_real_name(recipe_name)
    recipe = get_recipe_by_name(real_name)
    desc = f'Receta vegana y saludable: {recipe.name}. {recipe.intro}'
    keywords = get_recipe_keywords(recipe)
    return render_template('recipe.html',
                           title=recipe.name,
                           recipe_form=RecipesForm(),
                           recipe=recipe,
                           is_recipe=True,
                           last_recipes=get_last_recipes(4),
                           description=desc,
                           keywords=keywords)
