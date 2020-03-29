from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required

from syp.ingredients.forms import IngredientsForm
from syp.ingredients import utils, search
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


@ingredients.route("/subrecetas")
@login_required
def overview():
    """ Shows a list with all subrecipes. """
    return render_template(
        "ingredients.html",
        title="Subrecetas",
        recipe_form=SearchRecipeForm(),
        last_recipes=get_last_recipes(4),
        ingredients=utils.get_paginated_ingredients()[1],
    )
