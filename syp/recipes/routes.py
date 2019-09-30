from flask import Blueprint, render_template, flash, redirect, url_for
from syp.recipes import utils
from syp.ingredients.utils import get_all_ingredients
from syp.search.forms import SearchRecipeForm
from syp.recipes.forms import RecipeForm
from syp.models import Season, Subrecipe, Unit
import sys


recipes = Blueprint('recipes', __name__)


@recipes.route('/receta/<recipe_url>',
               methods=['GET', 'POST'])
def get_recipe(recipe_url):
    recipe = utils.get_recipe_by_url(recipe_url)
    desc = f'Receta vegana y saludable: {recipe.name}. {recipe.intro}'
    return render_template(
        'recipe.html',
        title=recipe.name,
        recipe_form=SearchRecipeForm(),
        recipe=recipe,
        is_recipe=True,
        last_recipes=utils.get_last_recipes(4),
        description=desc,
        keywords=utils.get_recipe_keywords(recipe)
    )


@recipes.route('/editar_receta/<recipe_url>',
               methods=['GET', 'POST'])
def edit_recipe(recipe_url):
    recipe = utils.get_recipe_by_url(recipe_url)
    form = RecipeForm(obj=recipe)
    form.season.choices = [(s.id, s.name) for s in
                           Season.query.order_by(Season.id.desc())]
    form.subrecipes.choices = [(r.id, r.name) for r in
                               Subrecipe.query.order_by(Subrecipe.name)]
    for subform in form.ingredients:
        subform.unit.choices = [(u.id, u.singular) for u in
                                Unit.query.order_by(Unit.singular)]
    if form.validate_on_submit():
        error = utils.form_errors(form)
        if error is None:
            flash('Los cambios han sido guardados.', 'success')
            new_url = utils.update_recipe(recipe, form)
            return redirect(url_for('recipes.get_recipe', recipe_url=new_url))
        else:
            flash(error, 'danger')

    desc = f'Receta vegana y saludable: {recipe.name}. {recipe.intro}'
    return render_template(
        'edit_recipe.html',
        form=form,
        title=recipe.name,
        recipe_form=SearchRecipeForm(),
        recipe=recipe,
        is_edit_recipe=True,
        all_ingredients=get_all_ingredients(),
        all_subrecipes=utils.get_all_subrecipes(),
        last_recipes=utils.get_last_recipes(4),
        description=desc,
        keywords=utils.get_recipe_keywords(recipe)
    )
