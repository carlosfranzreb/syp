""" Functions related to the creation of recipes, which means
writing new recipes to the DB. """


from flask_login import current_user

from syp.models.recipe import Recipe
from syp.recipes import update, utils
from syp.recipes.images import store_image
from syp import db


def save_recipe(form):
    """ Save newly created recipe. """
    recipe = Recipe(
        name=form.name.data,
        url=utils.get_url_from_name(form.name.data),
        id_user=current_user.id,
        id_state=form.state.data,
        id_season=form.season.data,
        time_prep=form.time_prep.data,
        time_cook=form.time_cook.data,
        intro=form.intro.data,
        text=form.text.data,
        health=form.health.data,
        link_video=form.link_video.data
    )
    db.session.add(recipe)
    db.session.commit()
    update.update_steps(recipe, form)
    update.update_ingredients(recipe, form)
    db.session.commit()
    if form.image.data:
        store_image(form.image.data, recipe.url)
    return recipe
