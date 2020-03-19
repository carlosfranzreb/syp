from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import login_required

from syp.subrecipes import utils
from syp.search.forms import SearchRecipeForm
from syp.recipes.utils import get_last_recipes
from syp.subrecipes.forms import SubrecipeForm


subrecipes = Blueprint("subrecipes", __name__)


@subrecipes.route("/subrecetas")
@login_required
def overview():
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
    form = SubrecipeForm()
    if form.validate_on_submit():
        # SAVE CHANGES
        flash("Los cambios han sido guardados.", "success")
        return redirect(url_for("subrecipes.overview"))
    return render_template(
        "edit_subrecipe.html",
        title="Subrecetas",
        recipe_form=SearchRecipeForm(),
        last_recipes=get_last_recipes(4),
        subrecipes=utils.get_paginated_subrecipes()[1],
        form=form,
    )
