from flask import Blueprint, render_template, redirect, url_for, flash, abort
from flask_login import login_required, current_user

from syp.ingredients.forms import IngredientsForm, IngredientForm, SearchForm
from syp.ingredients import utils, search, validate, update, create, overview
from syp.search.forms import SearchRecipeForm
from syp.recipes.utils import get_last_recipes

ingredients = Blueprint('ingredients', __name__)


@ingredients.route("/ingredientes/ordenar_por_nombre/desc_<arg>", methods=['GET', 'POST'])
@login_required
def sort_by_name(arg):
    """ Shows a list with all ingredients, ordered by name.
    Also, if the search form is submitted, it redirects to the
    search_by_name route."""
    form = SearchForm()
    if form.validate_on_submit():
        return redirect(url_for(
            'ingredients.search_by_name', arg=form.name.data
        ))
    return render_template(
        'overview/ingredient.html',
        title='Ingredientes',
        recipe_form=SearchRecipeForm(),
        last_recipes=get_last_recipes(4),
        ingredients=overview.sort_by_name(arg)[1],
        arg=arg,
        search_form=form
    )


@ingredients.route("/ingredients/buscar/<arg>")
@login_required
def search_by_name(arg):
    return render_template(
        'overview/ingredient.html',
        title='Ingredientes',
        recipe_form=SearchRecipeForm(),
        last_recipes=get_last_recipes(4),
        ingredients=overview.search_name(arg)[1],
        arg='True',
        search_form=SearchForm()
    )


@ingredients.route("/ingredientes/ordenar_por_fecha/desc_<arg>")
@login_required
def sort_by_date(arg):
    """ Shows a list with all ingredients of the user, ordered by date. """
    return render_template(
        "overview/ingredient.html",
        title="Ingredientes",
        recipe_form=SearchRecipeForm(),
        last_recipes=get_last_recipes(4),
        ingredients=overview.sort_by_date(arg)[1],
        arg=arg,
        search_form=SearchForm()
    )


@ingredients.route("/ingredientes/ordenar_por_fecha/desc_<arg>")
@login_required
def sort_by_creator(arg):
    """ Shows a list with all ingredients of the user, ordered by creator. """
    return render_template(
        "overview/ingredient.html",
        title="Ingredientes",
        recipe_form=SearchRecipeForm(),
        last_recipes=get_last_recipes(4),
        ingredients=overview.sort_by_creator(arg)[1],
        arg=arg,
        search_form=SearchForm()
    )


@ingredients.route('/buscar_por_ingrediente', methods=['GET', 'POST'])
def search_all_ingredients():
    """ Function that searchs for recipes that contain the given ingredient. """
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
        'search/ingredient.html',
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
        return redirect(url_for(
            'ingredients.search_ingredient', ing_url=ingredient.url
        ))
    ing = utils.get_ingredient_by_url(ing_url)
    page, recs = search.get_recipes_by_ingredient(ing.name)
    if isinstance(recs, str):
        flash(recs, 'danger')
        return redirect(url_for('ingredients.search_all_ingredients'))

    desc = f'Recetas veganas y saludables con {ing.name}. Por si se te antoja \
        {ing.name}, o lo compraste y buscas inspiración.'
    return render_template(
        'search/ingredient.html',
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
            return redirect(url_for('ingredients.sort_by_date', arg='True'))
    return render_template(
        "edit/ingredient.html",
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
            flash('El ingrediente ha sido creado.', 'success')
            return redirect(url_for('ingredients.sort_by_date', arg='True'))
    return render_template(
        "edit/ingredient.html",
        title="Crear ingrediente",
        ingredient=ingredient,
        recipe_form=SearchRecipeForm(),
        last_recipes=get_last_recipes(4),
        form=form,
        is_edit_recipe=True
    )


@ingredients.route("/borrar_ingrediente/<ingredient_url>")
@login_required
def delete_ingredient(ingredient_url):
    ingredient = utils.get_ingredient_by_url(ingredient_url)
    if ingredient.created_by != current_user.id:
        return abort(403)
    if ingredient.uses() > 0:
        flash('El ingrediente no se puede borrar. Hay recetas que lo usan.', 'danger')
    else:
        utils.delete_ingredient(ingredient)
        flash('El ingrediente ha sido borrado.', 'success')
    return redirect(url_for('ingredients.sort_by_date', arg='True'))
