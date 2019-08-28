from flask import Blueprint, flash, render_template, redirect, url_for
from syp.recipes.utils import get_paginated_recipes, get_last_recipes
from syp.search.forms import SearchRecipeForm
from syp.search.utils import get_recipes_by_name, get_default_keywords, \
                             get_search_keywords


search = Blueprint('search', __name__)


@search.route('/buscar', methods=['GET', 'POST'])
def search_all_recipes():
    form = SearchRecipeForm()
    if form.is_submitted():
        return redirect(url_for('search.search_recipe',
                                recipe_name=form.recipe.data))

    page, recs = get_paginated_recipes()
    desc = 'Todas nuestras recetas, veganas y saludables. Aquí encontrarás \
    platos muy variados, algunas rápidas, otras más elaboradas, pero todas \
    bien explicadas y con vídeo incluido.'
    return render_template('all.html',
                           title='Recetas',
                           recipe_form=SearchRecipeForm(),
                           recipes=recs,
                           last_recipes=get_last_recipes(4),
                           description=' '.join(desc.split()),
                           keywords=get_default_keywords())


@search.route('/buscar/<recipe_name>', methods=['GET', 'POST'])
def search_recipe(recipe_name):
    form = SearchRecipeForm()
    if form.is_submitted():
        return redirect(url_for('search.search_recipe',
                                recipe_name=form.recipe.data))

    page, recs = get_recipes_by_name(recipe_name)
    if isinstance(recs, str):
        flash(recs, 'danger')
        return redirect(url_for('search.search_all_recipes'))
    return render_template('all.html',
                           title=recipe_name,
                           recipe_form=SearchRecipeForm(),
                           recipes=recs,
                           last_recipes=get_last_recipes(),
                           keywords=get_search_keywords(recipe_name))
