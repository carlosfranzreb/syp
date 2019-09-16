from flask import Blueprint, render_template
from syp.recipes.utils import get_recipe_by_name, get_last_recipes, \
                              get_recipe_keywords, get_real_name, \
                              get_all_subrecipes, get_subrecipe
from syp.ingredients.utils import get_all_ingredients
from syp.search.forms import SearchRecipeForm
from syp.recipes.forms import RecipeForm
from syp.models import Season, Subrecipe, Unit
import sys


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
                           recipe_form=SearchRecipeForm(),
                           recipe=recipe,
                           is_recipe=True,
                           last_recipes=get_last_recipes(4),
                           description=desc,
                           keywords=keywords)


@recipes.route('/editar_receta/<recipe_name>',
               methods=['GET', 'POST'])
def edit_recipe(recipe_name):
    real_name = get_real_name(recipe_name)
    recipe = get_recipe_by_name(real_name)
    form = RecipeForm(obj=recipe)
    if form.validate_on_submit():
        print('Form is being validated', file=sys.stdout)
    else:
        desc = f'Receta vegana y saludable: {recipe.name}. {recipe.intro}'
        keywords = get_recipe_keywords(recipe)
        form.season.choices = [(s.id, s.name) for s in
                               Season.query.order_by(Season.id.desc())]
        form.subrecipes.choices = [(r.id, r.name) for r in
                                   Subrecipe.query.order_by(Subrecipe.name)]
        for subform in form.ingredients:
            subform.unit.choices = [(u.id, u.singular) for u in
                                    Unit.query.order_by(Unit.singular)]
        
        print(recipe.subrecipes, file=sys.stdout)
        return render_template('edit_recipe.html',
                               form=form,
                               title=recipe.name,
                               recipe_form=SearchRecipeForm(),
                               recipe=recipe,
                               is_edit_recipe=True,
                               all_ingredients=get_all_ingredients(),
                               all_subrecipes=get_all_subrecipes(),
                               last_recipes=get_last_recipes(4),
                               description=desc,
                               keywords=keywords)


@recipes.route('/receta/<recipe_name>',
               methods=['GET', 'POST'])
def save_recipe(recipe_name):
    real_name = get_real_name(recipe_name)
    recipe = get_recipe_by_name(real_name)
    desc = f'Receta vegana y saludable: {recipe.name}. {recipe.intro}'
    keywords = get_recipe_keywords(recipe)
    return render_template('edit_recipe.html',
                           title=recipe.name,
                           recipe_form=SearchRecipeForm(),
                           recipe=recipe,
                           is_recipe=True,
                           last_recipes=get_last_recipes(4),
                           description=desc,
                           keywords=keywords)
