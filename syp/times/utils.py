""" Help functions for the search-by-time page. """


from string import Template
from flask import request

from syp.models.recipe import Recipe
from syp.search.utils import get_default_keywords


def get_recipes_by_time(time, items=9):
    """ checks if input is number; returns recipes that can be
        done in that time, the closest to the given time goes firstself.
        If there are no recipes that are done quicker than the input time,
        another error message is displayed """
    try:
        minutes = int(time)
    except ValueError:
        return ('', Template('¡$time no es un número! Vuelve a intentarlo.')
                .substitute(time=time))

    page = request.args.get('page', 1, type=int)
    recipes = Recipe.query.filter(Recipe.time_cook +
                                  Recipe.time_prep <= minutes) \
                          .order_by((Recipe.time_prep +
                                     Recipe.time_cook).desc()) \
                          .paginate(page=page, per_page=items)

    if recipes.items == []:
        recipes = Template('No tenemos recetas que se hagan en menos de $time \
                            minutos. Dedícale un poco más de tiempo; \
                            no te arrepentirás').substitute(time=time)

    return (page, recipes)


def get_times_keywords(time=None):
    """ SEO keywords specific for this page. """
    times_keys = get_default_keywords()

    if time is not None:
        times_keys += f', receta vegana en {time} minutos, '
        times_keys += f'receta saludable en {time} minutos, '
        times_keys += f'receta casera en {time} minutos'

    times_keys += ', receta vegana rápida, receta saludable rápida, \
                   receta casera rápida'

    return ' '.join(times_keys.split())
