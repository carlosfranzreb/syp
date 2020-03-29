""" Help functions to validate ingredients. Name and URL must be unique. """


from syp.models.ingredient import Ingredient
from syp.recipes.utils import get_url_from_name


def validate_name(form):
    """ Validate the name and URL by checking if they are unique. """
    errors = list()
    name = form.name.data  # name of the subrecipe.
    url = get_url_from_name(name)
    if name == 'Nuevo ingrediente':
        errors.append(
            'Cambia el nombre del ingrediente donde pone "Nuevo ingrediente"'
        )
    elif Ingredient.query.filter_by(name=name).first() is not None:
        errors.append(
            f'Ya existe un ingrediente llamado "{name}". ¡Cambia el nombre!'
        )
    elif Ingredient.query.filter_by(url=url).first() is not None:
        errors.append(
            f'Ya existe un ingrediente cuyo URL es "{url}". ¡Cambia el nombre!'
        )
    return errors