from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import login_required

from syp.subrecipes import utils, update
from syp.search.forms import SearchRecipeForm
from syp.recipes.utils import get_last_recipes
from syp.subrecipes.forms import SubrecipeForm
from syp.models.unit import Unit


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
    if form.validate_on_submit():
        update.update_subrecipe(subrecipe, form)
        flash("Los cambios han sido guardados.", "success")
        return redirect(url_for("subrecipes.overview"))
    return render_template(
        "edit_subrecipe.html",
        title="Subrecetas",
        subrecipe=subrecipe,
        recipe_form=SearchRecipeForm(),
        last_recipes=get_last_recipes(4),
        subrecipes=utils.get_paginated_subrecipes()[1],
        form=form,
        is_edit_recipe=True
    )

@subrecipes.route("/borrar_subreceta/<subrecipe_url>")
@login_required
def delete_subrecipe(subrecipe_url):
    subrecipe = utils.get_subrecipe_by_url(subrecipe_url)
    if subrecipe.uses() > 0:
        flash('La subreceta no se puede borrar. Hay recetas que la usan.', 'danger')
    else:
        utils.delete_subrecipe(subrecipe)
        flash('La subreceta ha sido borrada.', 'success')
    return redirect(url_for('subrecipes.overview'))
