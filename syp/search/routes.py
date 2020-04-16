from flask import Blueprint, flash, render_template, redirect, url_for
from syp.recipes.utils import get_paginated_recipes, get_last_recipes
from syp.search.forms import SearchRecipeForm
from syp.search import utils


search = Blueprint('search', __name__)


@search.route('/buscar', methods=['GET', 'POST'])
def search_all_recipes():
    form = SearchRecipeForm()
    if form.is_submitted():
        return redirect(url_for(
            'search.search_recipe',
            recipe_name=form.recipe.data
        ))

    page, recs = get_paginated_recipes()
    desc = 'Todas nuestras recetas, veganas y saludables. Aquí encontrarás \
    platos muy variados, algunas rápidas, otras más elaboradas, pero todas \
    bien explicadas y con vídeo incluido.'
    return render_template(
        'search/recipe.html',
        title='Recetas',
        recipe_form=SearchRecipeForm(),
        recipes=recs,
        last_recipes=get_last_recipes(4),
        description=' '.join(desc.split()),
        keywords=utils.get_default_keywords()
    )


@search.route('/buscar/<recipe_name>', methods=['GET', 'POST'])
def search_recipe(recipe_name):
    form = SearchRecipeForm()
    if form.is_submitted():
        return redirect(url_for(
            'search.search_recipe',
            recipe_name=form.recipe.data
        ))
    page, recs = utils.get_recipes_by_name(recipe_name)
    if isinstance(recs, str):
        flash(recs, 'danger')
        return redirect(url_for('search.search_all_recipes'))
    return render_template(
        'search/recipe.html',
        title=recipe_name,
        recipe_form=SearchRecipeForm(),
        recipes=recs,
        last_recipes=get_last_recipes(),
        keywords=utils.get_search_keywords(recipe_name)
    )


@search.route('/<username>/recetas', methods=['GET', 'POST'])
def all_cook_recipes(username):
    form = SearchRecipeForm()
    if form.is_submitted():
        return redirect(url_for(
            'search.cook_recipe',
            username=username,
            recipe_name=form.recipe.data
        ))

    page, recs = utils.all_cook_recipes(username)
    desc = 'Todas nuestras recetas, veganas y saludables. Aquí encontrarás \
    platos muy variados, algunas rápidas, otras más elaboradas, pero todas \
    bien explicadas y con vídeo incluido.'
    return render_template(
        'search/cook_recipes.html',
        title=f'Recetas de {username}',
        form=form,
        username=username,
        recipe_form=SearchRecipeForm(),
        recipes=recs,
        cook_recipes=utils.cook_recipe_names(username),
        last_recipes=get_last_recipes(4),
        description=' '.join(desc.split()),
        keywords=utils.get_default_keywords()
    )


@search.route('/<username>/recetas/<recipe_name>', methods=['GET', 'POST'])
def cook_recipe(username, recipe_name):
    page, recs = utils.cook_recipes(username, recipe_name)
    if isinstance(recs, str):
        flash(recs, 'danger')
        return redirect(url_for(
            'search.all_cook_recipes',
            username=username
        ))
    return render_template(
        'search/cook_recipes.html',
        title=recipe_name,
        form=SearchRecipeForm(),  # form is submitted to all_cook_recipes()
        recipe_form=SearchRecipeForm(),  # sidebar form
        username=username,
        recipes=recs,
        cook_recipes=utils.cook_recipe_names(username),
        last_recipes=get_last_recipes(4),
        keywords=utils.get_search_keywords(recipe_name)
    )
