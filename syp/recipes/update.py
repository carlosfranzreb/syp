"""Functions to update recipes. """


from syp.models.quantity import Quantity
from syp.models.ingredient import Ingredient
from syp.models.subrecipe import Subrecipe
from syp.models.unit import Unit
from syp.models.recipe_step import RecipeStep
from syp.recipes.images import change_image
from syp import db


def update_recipe(recipe, form):
    """ Find changes and update the appropriate elements. 
    Calls functions to update ingredients, steps, subrecipes and images. """
    if recipe.name != form.name.data:
        old_url = recipe.url
        new_name = form.name.data
        recipe.name = new_name
        recipe.url = get_url_from_name(new_name)
        if form.image.data:  # new image,  new name
            change_image(form.image.data, recipe.url, old_url)
        else:  # same image, new name
            change_image(None, recipe.url, old_url)
    elif form.image.data:  # new image, same name
        change_image(form.image.data, None, recipe.url)
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
        recipe.id_state = form.state.data   
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
            quantity = Quantity(
                amount=subform.amount.data,
                id_recipe=recipe.id,
                id_ingredient=new_ing.id,
                id_unit=subform.unit.data
            )
            db.session.add(quantity)
    for ing_name in deleted_ings:  # remove deleted quantities
        removed_q = recipe.ingredients[deleted_ings.index(ing_name)]
        db.session.delete(removed_q)


def update_steps(recipe, form):
    """ Update steps. """
    old_steps = [s.step for s in recipe.steps]
    deleted_steps = old_steps.copy()
    for idx, subform in enumerate(form.steps):
        step_name = subform.step.data
        if 'Receta: ' in step_name:  # step is a subrecipe
            step_name = step_name[8:]  # Remove 'Receta: '
            subrecipe = Subrecipe.query.filter_by(
                name=step_name
            ).first()
            if subrecipe.id in old_steps:  # change step nr
                step = recipe.steps[old_steps.index(step_name)]
                deleted_steps.remove(step_name)
                step.step_nr = idx + 1
            else:  # create new step for subrecipe
                recipe.steps.append(RecipeStep(
                        step_nr=idx+1,
                        step=subrecipe.id,
                        id_recipe=recipe.id
                ))
        else:  # step is not a subrecipe
            if step_name in old_steps:  # change step_nr
                step = recipe.steps[old_steps.index(step_name)]
                deleted_steps.remove(step_name)
                step.step_nr = idx + 1
            else:  # create new step
                recipe.steps.append(RecipeStep(
                        step_nr=idx+1,
                        step=step_name,
                        id_recipe=recipe.id
                ))
    for step_name in deleted_steps:  # remove deleted steps
        for step in recipe.steps:
            if step.step == step_name:
                db.session.delete(step)


def get_url_from_name(name):
    """ Help function. """
    name = name.lower()
    replacements = {'ñ': 'n', 'í': 'i', 'ó': 'o',
                    'é': 'e', 'ú': 'u', 'á': 'a'}
    for char in name:
        if char in replacements.keys():
            name = name.replace(char, replacements[char])
    return name.replace(' ', '_')
