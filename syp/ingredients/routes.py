from flask import Blueprint, render_template, redirect, url_for, flash
from syp.ingredients.forms import IngredientsForm
from syp.ingredients import utils
from syp.search.forms import SearchRecipeForm
from syp.recipes.utils import get_last_recipes

ingredients = Blueprint('ingredients', __name__)


@ingredients.route('/ingrediente', methods=['GET', 'POST'])
def search_all_ingredients():
    form = IngredientsForm()
    if form.is_submitted():
        return redirect(url_for('ingredients.search_ingredient',
                                ing_name=form.ingredient.data))

    desc = 'Busca recetas veganas y saludables que contengan un ingrediente. \
            Por si tienes algún capricho, o un ingrediente con el que no \
            sabes qué hacer.'
    return render_template('ingredients.html',
                           title='Ingredientes',
                           recipe_form=SearchRecipeForm(),
                           form=form,
                           all_ingredients=utils.get_all_ingredients(),
                           recipes=None,
                           last_recipes=get_last_recipes(4),
                           description=' '.join(desc.split()),
                           keywords=utils.get_ing_keywords())


@ingredients.route('/ingrediente/<ing_name>', methods=['GET', 'POST'])
def search_ingredient(ing_name):
    form = IngredientsForm()
    if form.is_submitted():
        return redirect(url_for('ingredients.search_ingredient',
                                ing_name=form.ingredient.data))

    page, recs = utils.get_recipes_by_ingredient(ing_name)
    if isinstance(recs, str):
        flash(recs, 'danger')
        return redirect(url_for('ingredients.search_all_ingredients'))

    desc = f'Recetas veganas y saludables con {ing_name}. Por si se te antoja \
             {ing_name}, o lo compraste y buscas inspiración.'
    return render_template('ingredients.html',
                           title=ing_name,
                           recipe_form=SearchRecipeForm(),
                           form=form,
                           all_ingredients=utils.get_all_ingredients(),
                           recipes=recs,
                           last_recipes=get_last_recipes(4),
                           description=' '.join(desc.split()),
                           keywords=utils.get_ing_keywords(ing_name))
