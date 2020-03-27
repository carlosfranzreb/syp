""" Help functions to validate subrecipes.
Name must be unique for each user.
Ingredients must be chosen from the list.
At least one non-empty step. Max. length of steps is checked by the form. """


from syp.models.subrecipe import Subrecipe
from syp.models.ingredient import Ingredient
from syp.recipes.utils import get_url_from_name


def validate(form):
    """ Validate the name and URL by checking if they are unique
    and call a function to validate the ingredients. """
    errors = list()
    name = form.name.data  # name of the subrecipe.
    url = get_url_from_name(name)
    if name == 'Nueva subreceta':
        errors.append(
            'Cambia el nombre de la subreceta donde pone "Nueva subreceta"'
        )
    elif Subrecipe.query.filter_by(name=name).first() is not None:
        errors.append(
            f'Ya existe una subreceta llamada "{name}". Cambia el nombre!'
        )
    elif Subrecipe.query.filter_by(url=url).first() is not None:
        errors.append(
            f'Ya existe una subreceta cuya URL es "{url}". Cambia el nombre!'
        )
    return errors + validate_ingredients(form)


def validate_ingredients(form):
    """ Verify that all ingredients are part of the catalogue. """
    errors = list()
    for subquantity in form.ingredients.data:
        name = subquantity['ingredient']
        if (Ingredient.query.filter_by(name=name).first()) is None:
            errors.append(
                f'El ingrediente "{name}" no existe. Escoge uno de la lista.'
            )
    return errors

