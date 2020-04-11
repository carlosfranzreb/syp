""" Help function for recipe-related pages. """
#pylint: disable = missing-function-docstring


from flask import abort, request
from flask_login import current_user

from syp.utils.images import delete_image
from syp.search.utils import get_default_keywords
from syp.models.recipe import Recipe
from syp.models.subrecipe import Subrecipe
from syp.models.season import Season
from syp.models.unit import Unit
from syp.models.recipe_state import RecipeState

from syp import db


def get_recipe_by_name(recipe_name):
    recipe = Recipe.query \
        .filter_by(name=recipe_name) \
        .first()
    recipe.subrecipes = get_subrecipes(recipe)
    return discard_duplicates(recipe)


def get_recipe_by_url(recipe_url):
    recipe = Recipe.query \
        .filter_by(url=recipe_url) \
        .first()
    recipe.subrecipes = get_subrecipes(recipe)
    return discard_duplicates(recipe)


def discard_duplicates(recipe):
    if recipe is None:
        return abort(404)
    ingredient_ids = []
    for quantity in recipe.ingredients:
        quantity.duplicate = False
        ingredient_ids.append(quantity.ingredient.id)
    for sub in recipe.subrecipes:
        for quantity in sub.ingredients:
            ingredient_id = quantity.ingredient.id
            if ingredient_id not in ingredient_ids:
                quantity.duplicate = False
                ingredient_ids.append(ingredient_id)
            else:
                quantity.duplicate = True
    return recipe


def get_last_recipes(limit=None):
    """ returns published recipes starting with the most recent one
        Images are sized 300 (small)"""
    return Recipe.query \
        .filter_by(id_state=3) \
        .order_by(Recipe.created_at.desc()) \
        .limit(limit).all()


def get_paginated_recipes(limit=None, items=9):
    """ returns paginated recipes (published) starting with the most
        recent one. Images are medium sized (600). """
    page = request.args.get('page', 1, type=int)
    recipes = Recipe.query \
        .filter_by(id_state=3) \
        .order_by(Recipe.created_at.desc()) \
        .limit(limit).paginate(page=page, per_page=items)
    return (page, recipes)


def get_recipe_keywords(recipe):
    recipe_keys = get_default_keywords() + ', '
    for quantity in recipe.ingredients:
        name = quantity.ingredient.name.lower()
        recipe_keys += f'receta vegana con {name}, '
        recipe_keys += f'receta saludable con {name}, '
    return ' '.join(recipe_keys[:-2].split())


def get_all_subrecipes():
    """ Get all subrecipes of the user. """
    return Subrecipe.query \
        .filter_by(id_user=current_user.id) \
        .with_entities(Subrecipe.name) \
        .order_by(Subrecipe.name) \
        .all()


def get_all_units():
    """ Get all units. """
    return Unit.query \
        .with_entities(Unit.id, Unit.singular) \
        .order_by(Unit.singular) \
        .all()


def get_subrecipes(recipe):
    """ Get subrecipes used in the given recipe. If the step consists
    only of one int, then it is a reference to a subrecipe. """
    subrecipes = list()
    for step in recipe.steps:
        try:  # if the step is an int, it is a subrecipe.
            subrecipe_id = int(step.step)
            subrecipes.append(
                Subrecipe.query.filter_by(id=subrecipe_id).first()
            )
        except ValueError:  # Step is not a subrecipe.
            continue
    return subrecipes


def delete_recipe(recipe_id):
    """ Delete recipe by changing its state. Do delete the images
    as they take too much space. """
    recipe = Recipe.query.filter_by(id=recipe_id).first()
    delete_image(recipe.url, 'recipes')
    db.session.delete(recipe)
    db.session.commit()


def create_recipe():
    """ Returns new recipe to populate the empty form. """
    return Recipe(
        name="Nueva receta",
        url="nueva_receta",
        id_user=current_user.id
    )


def add_choices(form, recipe):
    """Add choices for the select fields (state, season and units)
    of the form, retrieved from the DB. Also select the units of
    the chosen ingredients, as found in the recipe object. """
    form.season.choices = [
        (s.id, s.name) for s in Season.query.order_by(Season.id.desc())
    ]
    form.state.choices = [
        (s.id, s.state) for s in RecipeState.query.order_by(RecipeState.id)
    ]
    for subform in form.ingredients:
        subform.unit.choices = [
            (u.id, u.singular) for u in Unit.query.order_by(Unit.singular)
        ]
        for quantity in recipe.ingredients:
            if quantity.ingredient.name == str(subform.ingredient.data):
                subform.unit.process_data(quantity.unit.id)
                break
    return form


def get_url_from_name(name):
    """ Help function. """
    name = name.lower()
    replacements = {'ñ': 'n', 'í': 'i', 'ó': 'o',
                    'é': 'e', 'ú': 'u', 'á': 'a'}
    for char in name:
        if char in replacements.keys():
            name = name.replace(char, replacements[char])
    return name.replace(' ', '_')
