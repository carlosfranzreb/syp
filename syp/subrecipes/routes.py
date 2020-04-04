from flask import Blueprint, render_template, flash, redirect, url_for, abort
from flask_login import login_required, current_user

from syp.subrecipes import utils, update, create, validate, overview
from syp.search.forms import SearchRecipeForm
from syp.recipes.utils import get_last_recipes, get_all_units
from syp.subrecipes.forms import SubrecipeForm, SearchForm
from syp.models.unit import Unit
from syp.ingredients.utils import get_all_ingredients


subrecipes = Blueprint("subrecipes", __name__)


@subrecipes.route("/subrecetas/ordenar_por_nombre/desc_<arg>", methods=['GET', 'POST'])
@login_required
def sort_by_name(arg):
    """ Shows a list with all subrecipes of the user, ordered by name.
    Also, if the search form is submitted, it redirects to the
    search_by_name route."""
    form = SearchForm()
    if form.validate_on_submit():
        return redirect(url_for(
            'subrecipes.search_by_name', arg=form.name.data
        ))
    return render_template(
        'overview_subrecipe.html',
        title='Subrecetas',
        recipe_form=SearchRecipeForm(),
        last_recipes=get_last_recipes(4),
        subrecipes=overview.sort_by_name(arg)[1],
        arg=arg,
        search_form=form
    )


@subrecipes.route("/subrecetas/buscar/<arg>")
@login_required
def search_by_name(arg):
    return render_template(
        'overview_subrecipe.html',
        title='Subrecetas',
        recipe_form=SearchRecipeForm(),
        last_recipes=get_last_recipes(4),
        subrecipes=overview.search_name(arg)[1],
        arg='True',
        search_form=SearchForm()
    )


@subrecipes.route("/subrecetas/ordenar_por_fecha/desc_<arg>")
@login_required
def sort_by_date(arg):
    """ Shows a list with all subrecipes of the user, ordered by date. """
    return render_template(
        "overview_subrecipe.html",
        title="Subrecetas",
        recipe_form=SearchRecipeForm(),
        last_recipes=get_last_recipes(4),
        subrecipes=overview.sort_by_date(arg)[1],
        arg=arg,
        search_form=SearchForm()
    )


@subrecipes.route("/editar_subreceta/<subrecipe_url>", methods=["GET", "POST"])
@login_required
def edit_subrecipe(subrecipe_url):
    subrecipe = utils.get_subrecipe_by_url(subrecipe_url)
    if subrecipe.id_user != current_user.id:
        return abort(404)
    form = SubrecipeForm(obj=subrecipe)
    for subform in form.ingredients:
        subform.unit.choices = [
            (u.id, u.singular) for u in Unit.query.order_by(Unit.singular)
        ]
    form.case.choices = [(0, "el"), (1, "la")]  # Set case choices.
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
            return redirect(url_for("subrecipes.sort_by_date", arg='True'))
    return render_template(
        "edit_subrecipe.html",
        title="Editar subreceta",
        subrecipe=subrecipe,
        recipe_form=SearchRecipeForm(),
        all_ingredients=get_all_ingredients(),
        all_units=get_all_units(),
        last_recipes=get_last_recipes(4),
        form=form,
        is_edit_recipe=True
    )

@subrecipes.route("/borrar_subreceta/<subrecipe_url>")
@login_required
def delete_subrecipe(subrecipe_url):
    subrecipe = utils.get_subrecipe_by_url(subrecipe_url)
    if subrecipe.id_user != current_user.id:
        return abort(404)
    if subrecipe.uses() > 0:
        flash('La subreceta no se puede borrar. Hay recetas que la usan.', 'danger')
    else:
        utils.delete_subrecipe(subrecipe)
        flash('La subreceta ha sido borrada.', 'success')
    return redirect(url_for("subrecipes.sort_by_date", arg='True'))


@subrecipes.route('/nueva_subreceta', methods=['GET', 'POST'])
@login_required
def create_subrecipe():
    subrecipe = utils.create_subrecipe()
    form = SubrecipeForm(obj=subrecipe)
    for subform in form.ingredients:
        subform.unit.choices = [
        (u.id, u.singular) for u in Unit.query.order_by(Unit.singular)
    ]
    form.case.choices = [(0, "el"), (1, "la")]  # Set case choices.
    if form.validate_on_submit():
        errors = validate.validate(form)
        if len(errors) > 0:
            for error in errors:
                flash(error, 'danger')
        else:
            create.save_subrecipe(form)
            flash('La subreceta ha sido creada.', 'success')
            return redirect(url_for("subrecipes.sort_by_date", arg='True'))
    return render_template(
        "edit_subrecipe.html",
        title="Crear subreceta",
        subrecipe=subrecipe,
        recipe_form=SearchRecipeForm(),
        last_recipes=get_last_recipes(4),
        all_ingredients=get_all_ingredients(),
        all_units=get_all_units(),
        form=form,
        is_edit_recipe=True,
        is_new_subrecipe=True
    )
