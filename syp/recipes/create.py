from flask_login import current_user

from syp.models.recipe import Recipe
from syp.recipes import update
from syp import db


def save_recipe(form):  # TODO: health is missing
    """ Save newly created recipe. """
    recipe = Recipe(
        name=form.name.data,
        url=update.get_url_from_name(form.name.data),
        id_user=current_user.id,
        id_state=form.state.data,
        id_season=form.season.data,
        time_prep=form.time_prep.data,
        time_cook=form.time_cook.data,
        intro=form.intro.data,
        text=form.text.data,
        link_video=form.link_video.data
    )
    db.session.add(recipe)
    db.session.commit()
    update.update_steps(recipe, form)
    update.update_ingredients(recipe, form)
    db.session.commit()
    if form.image.data:
        update.save_image(form.image.data, recipe.url)
    return recipe
