""" Help functions to update subrecipes. """


from datetime import datetime as dt

from syp.models.unit import Unit
from syp.models.subquantity import Subquantity
from syp.models.ingredient import Ingredient
from syp.models.subrecipe_step import SubrecipeStep
from syp.recipes.utils import get_url_from_name
from syp import db


def update_subrecipe(subrecipe, form):
    """ Updates name, ingredients and steps of subrecipe. """
    subrecipe.changed_at = dt.now()
    if subrecipe.name != form.name.data:
        new_name = form.name.data
        subrecipe.name = new_name
        subrecipe.url = get_url_from_name(new_name)
    if form.case.data != subrecipe.is_feminine:
        subrecipe.is_feminine = form.case.data
    update_ingredients(subrecipe, form)
    update_steps(subrecipe, form)
    db.session.commit()


def update_ingredients(subrecipe, form):
    """ Update ingredients. """
    old_ings = [q.ingredient.name for q in subrecipe.ingredients]
    deleted_ings = old_ings.copy()
    for subform in form.ingredients:
        ing_name = subform.ingredient.data
        if ing_name in old_ings:  # modify old subquantity
            ing = subrecipe.ingredients[old_ings.index(ing_name)]
            deleted_ings.remove(ing_name)
            if ing.amount != subform.amount.data:
                ing.amount = subform.amount.data
            if ing.unit.id != subform.unit.data:
                ing.unit = Unit.query.filter_by(id=subform.unit.data).first()
        else:  # create new subquantity
            new_ing = Ingredient.query.filter_by(name=ing_name).first()
            quantity = Subquantity(
                amount=subform.amount.data,
                id_subrecipe=subrecipe.id,
                id_ingredient=new_ing.id,
                id_unit=subform.unit.data
            )
            db.session.add(quantity)
    for ing_name in deleted_ings:  # remove deleted subquantities
        ing = Ingredient.query.filter_by(name=ing_name).first()
        db.session.delete(
            Subquantity.query
            .filter_by(id_subrecipe=subrecipe.id)
            .filter_by(id_ingredient=ing.id)
            .first()
        )


def update_steps(subrecipe, form):
    """ Update steps. """
    old_steps = [s.step for s in subrecipe.steps]
    deleted_steps = old_steps.copy()
    for idx, subform in enumerate(form.steps):
        step_name = subform.step.data
        if step_name in old_steps:  # change step_nr
            step = subrecipe.steps[old_steps.index(step_name)]
            deleted_steps.remove(step_name)
            step.step_nr = idx + 1
        else:  # create new step
            subrecipe.steps.append(SubrecipeStep(
                    step_nr=idx+1,
                    step=step_name,
                    id_subrecipe=subrecipe.id
            ))
    for step_name in deleted_steps:  # remove deleted steps
        for step in subrecipe.steps:
            if step.step == step_name:
                db.session.delete(step)