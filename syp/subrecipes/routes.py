from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import login_required

from syp.subrecipes import utils, update, create, validate
from syp.search.forms import SearchRecipeForm
from syp.recipes.utils import get_last_recipes
from syp.subrecipes.forms import SubrecipeForm
from syp.models.unit import Unit
from syp.ingredients.utils import get_all_ingredients


subrecipes = Blueprint("subrecipes", __name__)


@subrecipes.route("/subrecetas")
@login_required
def overview():
    """ Shows a list with all subrecipes. """
    return render_template(
        "subrecipes.html",
        title="Subrecetas",
        recipe_form=SearchRecipeForm(),
        last_recipes=get_last_recipes(4),
        subrecipes=utils.get_paginated_subrecipes()[1],
    )


@subrecipes.route("/editar_subreceta/<subrecipe_url>", methods=["GET", "POST"])
@login_required
def edit_subrecipe(subrecipe_url):
    subrecipe = utils.get_subrecipe_by_url(subrecipe_url)
    form = SubrecipeForm(obj=subrecipe)
    for subform in form.ingredients:
        subform.unit.choices = [
            (u.id, u.singular) for u in Unit.query.order_by(Unit.singular)
        ]
    form.case.choices = [(0, "el"), (1, "la")]  # Set case choices.
    if form.case.data is None:  # form is being served, not received.
        form.case.process_data(int(subrecipe.is_feminine))  # populate field.
    if form.validate_on_submit():
        if form.name.data != subrecipe.name:
            errors = validate.validate(form)
        else:  # if name hasn't changed, check only ingredients.
            errors = validate.validate_ingredients(form)
        if len(errors) > 0:
            for error in errors:
                flash(error, 'danger')
        else:
            update.update_subrecipe(subrecipe, form)
            flash("Los cambios han sido guardados.", "success")
            return redirect(url_for("subrecipes.overview"))
    return render_template(
        "edit_subrecipe.html",
        title="Editar subreceta",
        subrecipe=subrecipe,
        recipe_form=SearchRecipeForm(),
        all_ingredients=get_all_ingredients(),
        last_recipes=get_last_recipes(4),
        form=form,
        is_edit_recipe=True
    )

@subrecipes.route("/borrar_subreceta/<subrecipe_url>")
@login_required
def delete_subrecipe(subrecipe_url):
    # TODO: Window alert before deleting.
    subrecipe = utils.get_subrecipe_by_url(subrecipe_url)
    if subrecipe.uses() > 0:
        flash('La subreceta no se puede borrar. Hay recetas que la usan.', 'danger')
    else:
        utils.delete_subrecipe(subrecipe)
        flash('La subreceta ha sido borrada.', 'success')
    return redirect(url_for('subrecipes.overview'))


@subrecipes.route('/<subrecipe_url>', methods=['GET', 'POST'])
@login_required
def create_subrecipe(subrecipe_url):
    subrecipe = utils.create_subrecipe()
    form = SubrecipeForm(obj=subrecipe)
    for subform in form.ingredients:
        subform.unit.choices = [
        (u.id, u.singular) for u in Unit.query.order_by(Unit.singular)
    ]
    if form.validate_on_submit():
        errors = validate.validate(form)
        if len(errors) > 0:
            for error in errors:
                flash(error, 'danger')
        else:
            create.save_subrecipe(form)
            flash('La nueva subreceta ha sido guardada.', 'success')
            return redirect(url_for('subrecipes.overview'))
    return render_template(
        "edit_subrecipe.html",
        title="Crear subreceta",
        subrecipe=subrecipe,
        recipe_form=SearchRecipeForm(),
        last_recipes=get_last_recipes(4),
        all_ingredients=get_all_ingredients(),
        form=form,
        is_edit_recipe=True,
        is_new_subrecipe=True
    )


