""" Routing for everything related to recipes. """
# pylint: disable = invalid-name, missing-function-docstring


from flask import Blueprint, render_template, flash, redirect, url_for, abort
from flask_login import login_required, current_user

from syp.recipes import utils, update, validate, create
from syp.ingredients.utils import get_all_ingredients
from syp.search.forms import SearchRecipeForm
from syp.recipes.forms import RecipeForm, NewRecipeForm


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
        recipes=utils.get_overview_recipes()[1],
    )


@recipes.route(
    '/editar_receta/<recipe_url>',
    defaults={'state': None},
    methods=['GET', 'POST']
)
@recipes.route('/editar_receta/<recipe_url>/<state>', methods=['GET', 'POST'])
@login_required
def edit_recipe(recipe_url, state=None):
    """Edit a finished recipe, or one that is supposed to be so. The state
    argument is used by edit_new_recipe(), where the stored state is still 1,
    in case the recipe is not valid. The given state populates the form and
    only enters the DB if the recipe is valid. 
    State is set to 'edit' when the RecipeForm is posted and the validation
    should proceed, instead of redirecting to edit_new_recipe. """
    recipe = utils.get_recipe_by_url(recipe_url)
    if recipe.id_user != current_user.id:
        return abort(404)
    if state is None and recipe.id_state == 1:  # unfinished recipe
        return redirect(url_for(
            'recipes.edit_new_recipe',
            recipe_url=recipe_url
        ))
    form = utils.add_choices(RecipeForm(obj=recipe))
    if state is not None and state != 'edit':  # Add new state to form.
        form.state.process_data(int(state))
        form.validate()
    if form.validate_on_submit():
        errors = validate.validate_name(form, recipe) + \
            validate.validate_edition(form)
        if len(errors) == 0:
            flash('Los cambios han sido guardados.', 'success')
            return redirect(url_for(
                'recipes.get_recipe',
                recipe_url=update.update_recipe(recipe, form)
            ))
        for error in errors:
            flash(error, 'danger')
    return render_template(
        'edit_recipe.html',
        form=form,
        title=recipe.name,
        recipe_form=SearchRecipeForm(),
        recipe=recipe,
        is_edit_recipe=True,
        all_ingredients=get_all_ingredients(),
        all_subrecipes=utils.get_all_subrecipes(),
        all_units=utils.get_all_units(),
        last_recipes=utils.get_last_recipes(4),
        description=f'Receta vegana y saludable: {recipe.name}. {recipe.intro}',
        keywords=utils.get_recipe_keywords(recipe),
        state=state
    )


@recipes.route('/editar_nueva_receta/<recipe_url>', methods=['GET', 'POST'])
@login_required
def edit_new_recipe(recipe_url):
    """ Recipe state = 'Unfinished'. Validation is not thorough. """
    recipe = utils.get_recipe_by_url(recipe_url)
    if recipe.id_user != current_user.id:
        return abort(404)
    form = utils.add_choices(NewRecipeForm(obj=recipe))
    if form.validate_on_submit():
        errors = validate.validate_name(form, recipe)
        if len(errors) == 0:
            recipe_url = update.update_recipe(recipe, form, valid=False)
            if form.state.data == 1:  # create recipe and leave it unfinished
                return redirect(url_for('recipes.overview'))
            return redirect(url_for(  # check if it is ready for publishing
                'recipes.edit_recipe',
                recipe_url=recipe_url,
                state=form.state.data
            ))
        for error in errors:
            flash(error, 'danger')
    return render_template(
        'edit_recipe.html',
        form=form,
        title=recipe.name,
        recipe_form=SearchRecipeForm(),
        recipe=recipe,
        is_edit_recipe=True,
        all_ingredients=get_all_ingredients(),
        all_subrecipes=utils.get_all_subrecipes(),
        all_units=utils.get_all_units(),
        last_recipes=utils.get_last_recipes(4),
        description=f'Receta vegana y saludable: {recipe.name}. {recipe.intro}',
        keywords=utils.get_recipe_keywords(recipe),
        is_new_recipe=True
    )


@recipes.route('/nueva_receta', methods=['GET', 'POST'])
@login_required
def create_recipe():
    """ NewRecipeForm doesn't have requirements, so it can be saved unfinished. """
    recipe = utils.create_recipe()
    form = utils.add_choices(NewRecipeForm(obj=recipe))
    if form.validate_on_submit():
        errors = validate.validate_name(form)
        if len(errors) == 0:
            recipe = create.save_recipe(form, valid=False)
            if form.state.data == 1:
                return redirect(url_for('recipes.overview'))
            return redirect(url_for(  # check if ready for publishing.
                'recipes.edit_recipe',
                recipe_url=recipe.url,
                state=form.state.data
            ))
        for error in errors:
            flash(error, 'danger')
    return render_template(
        "edit_recipe.html",
        title="Crear receta",
        recipe=recipe,
        recipe_form=SearchRecipeForm(),
        last_recipes=utils.get_last_recipes(4),
        all_ingredients=get_all_ingredients(),
        all_subrecipes=utils.get_all_subrecipes(),
        all_units=utils.get_all_units(),
        form=form,
        is_edit_recipe=True
    )


@recipes.route("/borrar_receta/<recipe_url>")
@login_required
def delete_recipe(recipe_url):
    recipe = utils.get_recipe_by_url(recipe_url)
    utils.delete_recipe(recipe.id)
    flash('La receta ha sido borrada.', 'success')
    return redirect(url_for('recipes.overview'))
