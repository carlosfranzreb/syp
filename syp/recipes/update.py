"""Functions to update recipes. """


from datetime import datetime as dt

from syp.models.quantity import Quantity
from syp.models.ingredient import Ingredient
from syp.models.subrecipe import Subrecipe
from syp.models.unit import Unit
from syp.models.recipe_step import RecipeStep
from syp.utils import images
from syp.recipes.utils import get_url_from_name
from syp import db


def update_recipe(recipe, form, valid=True):
    """ Find changes and update the appropriate elements. 
    Calls functions to update ingredients, steps, subrecipes and images. """
    recipe.changed_at = dt.now()
    if recipe.name != form.name.data:
        old_url = recipe.url
        new_name = form.name.data
        recipe.name = new_name
        recipe.url = get_url_from_name(new_name)
        if form.image.data:  # new image,  new name
            images.change_image(form.image.data, 'recipes', recipe.url, old_url)
        else:  # same image, new name
            images.change_image(None, 'recipes', recipe.url, old_url)
    elif form.image.data:  # new image, same name
        images.change_image(form.image.data, 'recipes', None, recipe.url)
    if recipe.intro != form.intro.data:
        recipe.intro = form.intro.data
    if recipe.text != form.text.data:
        recipe.text = form.text.data
    if recipe.health != form.health.data:
        recipe.health = form.health.data
    if recipe.link_video != form.link_video.data:
        recipe.link_video = form.link_video.data
    if recipe.time_cook != form.time_cook.data:
        recipe.time_cook = form.time_cook.data
    if recipe.time_prep != form.time_prep.data:
        recipe.time_prep = form.time_prep.data
    if recipe.id_season != form.season.data:
        recipe.id_season = form.season.data
    if recipe.id_state != form.state.data:
        if valid or form.state.data == 1:
            recipe.id_state = form.state.data
            if recipe.id_state == 3:
                recipe.published_at = dt.now()
    update_ingredients(recipe, form)
    update_steps(recipe, form)
    db.session.commit()
    return recipe.url


def update_ingredients(recipe, form):
    """ Update ingredients. """
    old_ings = [q.ingredient.name for q in recipe.ingredients]
    deleted_ings = old_ings.copy()
    for subform in form.ingredients:
        ing_name = subform.ingredient.data
        if ing_name in old_ings:  # modify old quantity
            ing = recipe.ingredients[old_ings.index(ing_name)]
            deleted_ings.remove(ing_name)
            if ing.amount != subform.amount.data:
                ing.amount = subform.amount.data
            if ing.unit.id != subform.unit.data:
                ing.unit = Unit.query.filter_by(id=subform.unit.data).first()
        else:  # create new quantity
            new_ing = Ingredient.query.filter_by(name=ing_name).first()
            db.session.add(Quantity(
                amount=subform.amount.data,
                id_recipe=recipe.id,
                id_ingredient=new_ing.id,
                id_unit=subform.unit.data
            ))
    for ing_name in deleted_ings:  # remove deleted quantities
        ing = Ingredient.query.filter_by(name=ing_name).first()
        db.session.delete(
            Quantity.query
            .filter_by(id_recipe=recipe.id)
            .filter_by(id_ingredient=ing.id)
            .first()
        )


def update_steps(recipe, form):
    """ Update steps. """
    old_steps = [s.step for s in recipe.steps]
    deleted_steps = old_steps.copy()
    for idx, subform in enumerate(form.steps):
        step_data = subform.step.data
        if 'Receta: ' in step_data:  # step is a subrecipe
            step_data = step_data[8:]  # Remove 'Receta: '
            subrecipe = Subrecipe.query.filter_by(
                name=step_data
            ).first()
            if subrecipe.id in old_steps:  # change step nr
                step = recipe.steps[old_steps.index(step_data)]
                deleted_steps.remove(step_data)
                step.step_nr = idx + 1
            else:  # create new step for subrecipe
                new_step = RecipeStep(
                    step_nr=idx+1,
                    step=subrecipe.id,
                    id_recipe=recipe.id
                )
                db.session.add(new_step)
                recipe.steps.append(new_step)
        else:  # step is not a subrecipe
            if step_data in old_steps:  # change step_nr
                step = recipe.steps[old_steps.index(step_data)]
                deleted_steps.remove(step_data)
                step.step_nr = idx + 1
            else:  # create new step
                new_step = RecipeStep(
                    step_nr=idx+1,
                    step=step_data,
                    id_recipe=recipe.id
                )
                db.session.add(new_step)
                recipe.steps.append(new_step)
    for step_data in deleted_steps:  # remove deleted steps
        for step in recipe.steps:
            if step.step == step_data:
                db.session.delete(step)
