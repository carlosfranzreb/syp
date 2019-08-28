from flask import abort, request
from syp.search.utils import get_default_keywords
from syp.models import Recipe, Quantity, Subquantity, Ingredient
import ast


def get_recipe_by_name(recipe_name):
    """
    Gets recipe with following attributes:
    recipe.id = int
    recipe.name - string
    recipe.img_name - Name of recipe with underscores instead of spaces,
        lowercase, and _opt at the end (this is done directly in the
        template)
    recipe.time_cook, recipe.time_prep - integers
    recipe.season - string (backref)
    recipe.intro, recipe.text - strings
    recipe.real_steps - list of strings, with subrecipes
        marked as 'subrecipe_name'
    recipe.substeps - dictionary with steps for subrecipes:
        ['name']: ['title', list of steps]
    recipe.link_video - string
    recipe.health - string
    recipe.ingredients - list of ingredients
        ingredient.name - string
        ingredient.amount - int
        ingredient.unit.name - string
        ingredient.health - string
    recipe.subingredients - list of tuples (title, ingredients (as above))
        title: "Para el/la subrecipe", used in the ingredient section
    """
    recipe = Recipe.query.filter_by(name=recipe_name).first()

    if recipe is None:
        abort(404)
    else:
        recipe.real_steps = ast.literal_eval(recipe.steps)
        recipe.ingredients = get_ingredients_of_recipe(recipe.id)

        substeps, subingredients = get_subrecipes_of_recipe(recipe)
        recipe.substeps = substeps
        recipe.subingredients = subingredients

        return recipe


def get_ingredients_of_recipe(id):
    """Get ingredients of a recipe with: name, amount, unit, health"""
    query_quantity = Quantity.query.filter_by(id_recipe=id).all()
    ings = []

    for q in query_quantity:
        ing = Ingredient.query.filter_by(id=q.id_ingredient).first()
        ing.amount = simplify(q.amount)
        ings.append(ing)

    return ings


def get_ingredients_of_subrecipe(recipe, id):
    """
    Get ingredients of a recipe with: name, amount, unit, health
    If ingredient already in recipe, mark as duplicate, so it is not
    shown twice in the health section.
    """
    query_quantity = Subquantity.query.filter_by(id_subrecipe=id).all()
    ingredients = []

    for q in query_quantity:
        ing = Ingredient.query.filter_by(id=q.id_ingredient).first()
        ing.amount = simplify(q.amount)
        if ing in recipe.ingredients:
            ing.duplicate = True
        else:
            ing.duplicate = False
        ingredients.append(ing)

    return ingredients


def get_subrecipes_of_recipe(recipe):
    """
    recipe.substeps - dictionary with steps for subrecipes:
        ['name']: ['title', list of steps]
        ingredient.name - string
    recipe.subingredients - list of tuples (title, ingredients (as above))
        title: "Para el/la subrecipe", used in the ingredient section
        ingredients:
            ing.name - string
            ing.amount - int
            ingredient.unit.name - string
            ingredient.health - string
    """
    substeps, subingredients = {}, []
    for sub in recipe.subrecipes:
        substeps[sub.name] = ast.literal_eval(sub.steps)
        ings = get_ingredients_of_subrecipe(recipe, sub.id)
        subingredients.append([f"Para {get_case(sub.case_fem)} \
                               {sub.name.lower()}:", ings])

    return (substeps, subingredients)


def get_last_recipes(limit=None):
    """ returns recipes starting with the most recent one
        Images are sized 300"""
    recipes = Recipe.query.order_by(Recipe.date_created.desc()) \
                          .limit(limit).all()

    return recipes


def get_paginated_recipes(limit=None, items=9):
    """ returns paginated recipes starting with the most recent one
        Images are medium sized"""
    page = request.args.get('page', 1, type=int)
    recipes = Recipe.query.order_by(Recipe.date_created.desc()) \
                          .limit(limit).paginate(page=page, per_page=items)

    return (page, recipes)


def get_recipe_keywords(recipe):
    recipe_keys = get_default_keywords() + ', '
    for ing in recipe.ingredients:
        recipe_keys += f'receta vegana con {ing.name}, '
        recipe_keys += f'receta saludable con {ing.name}, '

    return ' '.join(recipe_keys[:-2].split())


def get_real_name(url_name):
    return url_name.replace("_", " ")


def get_case(case_id):
    if case_id == 0:
        return "el"
    elif case_id == 1:
        return "la"
    else:
        raise ValueError


def simplify(amount):
    if amount < 1 or amount / int(amount) != 1:
        return amount
    else:
        return int(amount)
