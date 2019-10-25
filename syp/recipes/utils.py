from os import path
from PIL import Image
import sys

from flask import abort, request, current_app
from syp.search.utils import get_default_keywords
from syp.models import Recipe, Quantity, Subquantity, Ingredient, \
                       Subrecipe, Unit, subrecipes, RecipeStep
from syp import db


def get_recipe_by_name(recipe_name):
    recipe = Recipe.query.filter_by(name=recipe_name).first()
    return discard_duplicates(recipe)


def get_recipe_by_url(recipe_url):
    recipe = Recipe.query.filter_by(url=recipe_url).first()
    return discard_duplicates(recipe)


def discard_duplicates(recipe):
    if recipe is None:
        abort(404)
    else:
        ids = []
        for q in recipe.ingredients:
            q.duplicate = False
            ids.append(q.ingredient.id)
        for sub in recipe.subrecipes:
            for q in sub.ingredients:
                id = q.ingredient.id
                if id not in ids:
                    q.duplicate = False
                    ids.append(id)
                else:
                    q.duplicate = True
        return recipe


def get_last_recipes(limit=None):
    """ returns recipes starting with the most recent one
        Images are sized 300"""
    recipes = Recipe.query.order_by(Recipe.date_created.desc()) \
                          .limit(limit).all()

    return recipes


def get_paginated_recipes(limit=None, items=9):
    """ returns paginated recipes starting with the most recent one
        Images are medium sized"""
    page = request.args.get('page', 1, type=int)
    recipes = Recipe.query.order_by(Recipe.date_created.desc()) \
                          .limit(limit).paginate(page=page, per_page=items)

    return (page, recipes)


def get_recipe_keywords(recipe):
    recipe_keys = get_default_keywords() + ', '
    for q in recipe.ingredients:
        name = q.ingredient.name.lower()
        recipe_keys += f'receta vegana con {name}, '
        recipe_keys += f'receta saludable con {name}, '
    return ' '.join(recipe_keys[:-2].split())


def get_all_subrecipes():
    return Subrecipe.query.with_entities(Subrecipe.name) \
                          .order_by(Subrecipe.name).all()


def get_subrecipe(id):
    return Subrecipe.query.filter_by(id=id).first()


def update_recipe(recipe, form):
    if recipe.name != form.name.data:
        new_name = form.name.data
        recipe.name = new_name
        recipe.url = get_url_from_name(new_name)
    if form.image.data:
        save_image(form.image.data, recipe.url)
    if recipe.intro != form.intro.data:
        recipe.intro = form.intro.data
    if recipe.text != form.text.data: 
        recipe.text = form.text.data
    if recipe.link_video != form.link_video.data:
        recipe.link_video = form.link_video.data

    recipe.subrecipes = [
        Subrecipe.query.filter_by(name=subform.subrecipe.data).first()
        for subform in form.subrecipes
    ]
    
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

    old_steps = [s.step for s in recipe.steps]
    deleted_steps = old_steps.copy()
    for idx, subform in enumerate(form.steps):
        step_name = subform.step.data
        if step_name in old_steps:  # change step_nr
            step = recipe.steps[old_steps.index(step_name)]
            deleted_steps.remove(step_name)
            if step.step_nr != idx + 1:
                step.step_nr = idx + 1
        else:  # create new step
            recipe.steps.append(
                RecipeStep(
                    step_nr=idx+1,
                    step=step_name,
                    id_recipe=recipe.id
                )
            )
    # remove deleted quantities
    for step_name in deleted_steps:
        for step in recipe.steps:
            if step.step == step_name:
                db.session.delete(step)
    #commit and return url for redirect
    db.session.commit()
    return recipe.url


def save_image(form_img, recipe_url):
    mark = Image.open(
        path.join(current_app.root_path, 'static/images/icons/syp_circle.png')
    )
    mark.thumbnail((250, 250))
    img = Image.open(form_img)
    img.paste(mark, (30, 30), mark)
    img = img.convert('RGB')
    img.save(
        path.join(
            current_app.root_path,
            f'static/images/recipes/large/{recipe_url}_opt.jpg'
        ),
        optimize=True,
        progressive=True
    )
    img.thumbnail((600, 600))
    img.save(
        path.join(
            current_app.root_path,
            f'static/images/recipes/600/{recipe_url}_600_opt.jpg'
        ),
        optimize=True,
        progressive=True
    )
    img.thumbnail((300, 300))
    img.save(
        path.join(
            current_app.root_path,
            f'static/images/recipes/300/{recipe_url}_300_opt.jpg'
        ),
        optimize=True,
        progressive=True
    )


def get_url_from_name(name):
    name = name.lower()
    replacements = {'ñ': 'n', 'í': 'i', 'ó': 'o',
                    'é': 'e', 'ú': 'u', 'á': 'a'}
    for char in name:
        if char in replacements.keys():
            char = replacements[char]
    return name.replace(' ', '_')


def form_errors(form):
    errors = list()
    # check if all ingredients are in the DB
    for subform in form.ingredients:
        ing_name = subform.ingredient.data
        if Ingredient.query.filter_by(name=ing_name).first() is None:
            errors.append(f"""El ingrediente "{ing_name}" no existe.
                Si está bien escrito, y no lo encuentras entre las opciones,
                crea un nuevo ingrediente.""")
    # Check if all subrecipes are used
    for subform in form.subrecipes:
        is_used = False
        subrecipe = subform.data['subrecipe']
        for step in form.steps:
            if step.data['step'] == subrecipe:
                is_used = True
        if not is_used:
            errors.append(f"""La subreceta '{subrecipe}' no está incluida en los
                pasos de la receta. Si no debería estarlo, bórrala de la
                sección 'Subrecetas'""")
    # Check if video link is correct
    video = form.link_video.data
    if len(video) > 0 and video[:30] !='https://www.youtube.com/embed/':
        errors.append("""Con ese link, el vídeo no se puede mostrar. Para conseguir
            el link correcto, haz click en 'Share' y luego en 'Embed' en la página 
            del vídeo.""")
    return errors
