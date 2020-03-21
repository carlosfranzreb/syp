""" Help functions for the search-by-name page. """


from flask import request
from string import Template

from syp.models.recipe import Recipe


def get_recipes_by_name(recipe_name, items=9):
    """ returns published recipes (not subrecipes) that contain the given name.
    Images are medium sized"""
    page = request.args.get('page', 1, type=int)
    recipes = Recipe.query.filter(Recipe.name.contains(recipe_name)) \
                          .filter_by(id_state=3) \
                          .order_by(Recipe.created_at.desc()) \
                          .paginate(page=page, per_page=items)
    if recipes.items == []:
        recipes = Template('No tenemos recetas llamadas $name. \
                         ¡Prueba con otra receta!') \
                        .substitute(name=recipe_name.lower())
    return (page, recipes)


def get_default_keywords():
    """ SEO keywords. """
    keys = "receta vegana, receta saludable, receta sana, plato vegano, \
            plato saludable, cocina vegana, receta casera vegana, \
            salud y pimienta, syp"
    return ' '.join(keys.split())


def get_search_keywords(recipe_name):
    """ SEO keywords specific for the search page. """
    search_keys = get_default_keywords()
    search_keys += f', {recipe_name} receta vegana, '
    search_keys += f'{recipe_name} receta saludable, '
    search_keys += f'{recipe_name} receta casera'
    return ' '.join(search_keys.split())
