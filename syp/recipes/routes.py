""" Routing for everything related to recipes. """
# pylint: disable = invalid-name, missing-function-docstring


from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import login_required

from syp.recipes import utils, update
from syp.ingredients.utils import get_all_ingredients
from syp.search.forms import SearchRecipeForm
from syp.recipes.forms import RecipeForm
from syp.models.season import Season
from syp.models.subrecipe import Subrecipe
from syp.models.unit import Unit
from syp.models.recipe_state import RecipeState


recipes = Blueprint('recipes', __name__)


@recipes.route('/receta/<recipe_url>', methods=['GET', 'POST'])
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


@recipes.route("/recetas")
@login_required
def overview():
    """ Shows a list with all recipes of the user. """
    return render_template(
        "recipes.html",
        title="Recetas",
        recipe_form=SearchRecipeForm(),
        last_recipes=utils.get_last_recipes(4),
        recipes=utils.get_paginated_recipes()[1],
    )


@recipes.route('/editar_receta/<recipe_url>', methods=['GET', 'POST'])
@login_required
def edit_recipe(recipe_url):
    recipe = utils.get_recipe_by_url(recipe_url)
    form = RecipeForm(obj=recipe)
    form.season.choices = [
        (s.id, s.name) for s in Season.query.order_by(Season.id.desc())
    ]
    form.subrecipes.choices = [
        (r.id, r.name) for r in Subrecipe.query.order_by(Subrecipe.name)
    ]
    form.state.choices = [
        (s.id, s.state) for s in RecipeState.query.order_by(RecipeState.id.desc())
    ]
    for subform in form.ingredients:
        subform.unit.choices = [(u.id, u.singular) for u in
                                Unit.query.order_by(Unit.singular)]
    if form.validate_on_submit():
        errors = update.form_errors(form)
        if len(errors) == 0:
            flash('Los cambios han sido guardados.', 'success')
            return redirect(url_for(
                'recipes.get_recipe',
                recipe_url=update.update_recipe(recipe, form)
            ))
        for error in errors:
            flash(error, 'danger')
    err = form.errors.items()
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
        description=f'Receta vegana y saludable: {recipe.name}. {recipe.intro}',
        keywords=utils.get_recipe_keywords(recipe)
    )


@recipes.route("/borrar_receta/<recipe_url>")
@login_required
def delete_recipe(recipe_url):
    # TODO: Window alert before deleting.
    recipe = utils.get_recipe_by_url(recipe_url)
    utils.delete_recipe(recipe.id)
    flash('La receta ha sido borrada.', 'success')
    return redirect(url_for('recipes.overview'))
