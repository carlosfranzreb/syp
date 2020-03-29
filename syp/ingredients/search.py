""" Help functions for search-by-ingredient pages. """


from string import Template
from flask import request

from syp.models.recipe import Recipe
from syp.models.recipe_step import RecipeStep
from syp.models.subrecipe import Subrecipe
from syp.models.quantity import Quantity
from syp.models.subquantity import Subquantity
from syp.models.ingredient import Ingredient


def get_recipes_by_ingredient(ing_name, items=9):
    """ Returns recipes by ingredient, the one that was created last goes first
    (ids in descent).
    If ingredient is in subrecipe, recipes that contain that subrecipe
    will be shown at the end.
    If $name is not an ingredient or a subrecipe, return error message
    If ingredient is found, but there are no recipes with it, that means
    that there was a recipe and it was deleted."""
    recipes = Recipe.query \
        .filter_by(id_state=3) \
        .join(Quantity, Recipe.id == Quantity.id_recipe) \
        .join(Ingredient, Quantity.id_ingredient == Ingredient.id) \
        .filter(Ingredient.name.contains(ing_name))
    recipes = recipes.union(get_subrecipes_by_ingredient(ing_name))
    page = request.args.get('page', 1, type=int)
    recipes = recipes.paginate(page=page, per_page=items)

    if recipes.items == []:
        recipes = Template(
            'No tenemos recetas con $name. ¡Prueba con otro ingrediente!'
        ).substitute(name=ing_name.lower())
    return (page, recipes)


def get_subrecipes_by_ingredient(ing):
    """Returns recipes that contain a subrecipe with the ingredient"""
    subs = Subrecipe.query \
        .join(Subquantity, Subrecipe.id == Subquantity.id_subrecipe) \
        .join(Ingredient, Subquantity.id_ingredient == Ingredient.id) \
        .filter(Ingredient.name.contains(ing)) \
        .all()
    # empty query, to extend in the for loop
    recipes = Recipe.query.filter_by(id=0)
    for subrecipe in subs:
        recipes = recipes.union(
            Recipe.query
            .join(RecipeStep, RecipeStep.id_recipe == Recipe.id)
            .filter(RecipeStep.step == subrecipe.id)
        )
    return recipes
