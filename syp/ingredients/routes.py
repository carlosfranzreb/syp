from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required

from syp.ingredients.forms import IngredientsForm, IngredientForm
from syp.ingredients import utils, search, validate, update, create
from syp.search.forms import SearchRecipeForm
from syp.recipes.utils import get_last_recipes

ingredients = Blueprint('ingredients', __name__)


@ingredients.route('/buscar_por_ingrediente', methods=['GET', 'POST'])
def search_all_ingredients():
    form = IngredientsForm()
    if form.is_submitted():
        ingredient = utils.get_ingredient_by_name(form.ingredient.data)
        return redirect(url_for(
            'ingredients.search_ingredient',
            ing_url=ingredient.url
        ))
    desc = 'Busca recetas veganas y saludables que contengan un ingrediente. \
        Por si tienes algún capricho, o un ingrediente con el que no \
        sabes qué hacer.'
    return render_template(
        'search_ingredients.html',
        title='Ingredientes',
        recipe_form=SearchRecipeForm(),
        form=form,
        all_ingredients=utils.get_all_ingredients(),
        recipes=None,
        last_recipes=get_last_recipes(4),
        description=' '.join(desc.split()),
        keywords=utils.get_ing_keywords()
    )


@ingredients.route('/recetas_con/<ing_url>', methods=['GET', 'POST'])
def search_ingredient(ing_url):
    form = IngredientsForm()
    if form.is_submitted():
        ingredient = utils.get_ingredient_by_name(form.ingredient.data)
        return redirect(url_for('ingredients.search_ingredient',
                                ing_url=ingredient.url))

    ing = utils.get_ingredient_by_url(ing_url)
    page, recs = search.get_recipes_by_ingredient(ing.name)
    if isinstance(recs, str):
        flash(recs, 'danger')
        return redirect(url_for('ingredients.search_all_ingredients'))

    desc = f'Recetas veganas y saludables con {ing.name}. Por si se te antoja \
        {ing.name}, o lo compraste y buscas inspiración.'
    return render_template(
        'search_ingredients.html',
        title=ing.name,
        chosen_url=ing_url,
        recipe_form=SearchRecipeForm(),
        form=form,
        all_ingredients=utils.get_all_ingredients(),
        recipes=recs,
        last_recipes=get_last_recipes(4),
        description=' '.join(desc.split()),
        keywords=utils.get_ing_keywords(ing.name)
    )


@ingredients.route("/ingredientes")
@login_required
def overview():
    """ Shows a list with all ingredients. """
    return render_template(
        "ingredients.html",
        title="Ingredientes",
        recipe_form=SearchRecipeForm(),
        last_recipes=get_last_recipes(4),
        ingredients=utils.get_paginated_ingredients()[1],
    )


@ingredients.route("/editar_ingrediente/<ingredient_url>", methods=["GET", "POST"])
@login_required
def edit_ingredient(ingredient_url):
    ingredient = utils.get_ingredient_by_url(ingredient_url)
    form = IngredientForm(obj=ingredient)
    if form.validate_on_submit():
        errors = list()
        if form.name.data != ingredient.name:
            errors = validate.validate_name(form)
        if len(errors) > 0:
            for error in errors:
                flash(error, 'danger')
        else:
            update.update_ingredient(ingredient, form)
            flash("Los cambios han sido guardados.", "success")
            return redirect(url_for("ingredients.overview"))
    return render_template(
        "edit_ingredient.html",
        title="Editar ingrediente",
        form=form,
        recipe_form=SearchRecipeForm(),
        last_recipes=get_last_recipes(4),
        ingredient=ingredient,
        is_edit_recipe=True
    )


@ingredients.route('/nuevo_ingrediente', methods=['GET', 'POST'])
@login_required
def create_ingredient():
    ingredient = utils.create_ingredient()
    form = IngredientForm(obj=ingredient)
    if form.validate_on_submit():
        errors = validate.validate_name(form)
        if len(errors) > 0:
            for error in errors:
                flash(error, 'danger')
        else:
            create.save_ingredient(form)
            flash('El nuevo ingrediente ha sido guardado.', 'success')
            return redirect(url_for('ingredients.overview'))
    return render_template(
        "edit_ingredient.html",
        title="Crear ingrediente",
        ingredient=ingredient,
        recipe_form=SearchRecipeForm(),
        last_recipes=get_last_recipes(4),
        form=form,
        is_edit_recipe=True
    )
