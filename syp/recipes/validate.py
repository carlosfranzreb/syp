from flask_login import current_user

from syp.models.ingredient import Ingredient
from syp.models.recipe import Recipe
from syp.recipes.utils import get_url_from_name


def validate_name(form, recipe=None):
    """ Validate the uniqueness of the name and URL. """
    name = form.name.data
    if recipe is not None and recipe.name == name:
        return list()  # It has already been validated.
    errors = list()
    url = get_url_from_name(name)
    query = Recipe.query.filter_by(id_user=current_user.id)
    if name == 'Nueva receta':
        errors.append(
            'Cambia el nombre de la receta donde pone "Nueva receta"'
        )
    elif query.filter_by(name=name).count() != 0:
        errors.append(
            f'Ya tienes una receta llamada "{name}". ¡Cambia el nombre!'
        )
    elif query.filter_by(url=url).count() != 0:
        errors.append(
            f'Ya tienes una receta cuya URL es "{url}". ¡Cambia el nombre!'
        )
    return errors

def validate_edition(form):
    """ Validate a form after an edition.
    Ensure that all ingredients are in the DB and the video link
    is correct. If not, return the appropiate errors. """
    errors = list()
    # check if all ingredients are in the DB.
    for subform in form.ingredients:
        ing_name = subform.ingredient.data
        if Ingredient.query.filter_by(name=ing_name).first() is None:
            errors.append(f"""El ingrediente "{ing_name}" no existe.
                Si está bien escrito, y no lo encuentras entre las opciones,
                crea un nuevo ingrediente.""")
    # Check if video link is correct.
    video = form.link_video.data
    if len(video) > 0 and video[:30] != 'https://www.youtube.com/embed/':
        errors.append("""Con ese link, el vídeo no se puede mostrar. Para conseguir
            el link correcto, haz click en 'Share' y luego en 'Embed' en la página 
            del vídeo.""")
    return errors