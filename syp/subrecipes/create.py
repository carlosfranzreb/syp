""" Help functions to create new subrecipes. """


from flask_login import current_user

from syp.recipes.update import get_url_from_name
from syp.models.subrecipe import Subrecipe
from syp.models.subrecipe_step import SubrecipeStep
from syp.models.ingredient import Ingredient
from syp.models.subquantity import Subquantity

from syp import db


def save_subrecipe(form):
    """ Save the newly created subrecipe. """
    subrecipe = Subrecipe(
        name=form.name.data,
        url=get_url_from_name(form.name.data),
        is_feminine=True,
        id_user=current_user.id,
    )
    db.session.add(subrecipe)
    db.session.commit()
    save_steps(form, subrecipe.id)
    save_ingredients(form, subrecipe.id)
    db.session.commit()


def save_steps(form, subrecipe_id):
    """ Saves the steps of the subrecipe. """
    step_nr = 1
    for step in form.steps.data:
        db.session.add(SubrecipeStep(
            step_nr=step_nr,
            step=step['step'],
            id_subrecipe=subrecipe_id
        ))
        step_nr += 1


def save_ingredients(form, subrecipe_id):
    """ Saves the ingredients of the subrecipe. """
    for subquantity in form.ingredients.data:
        ing = Ingredient.query.filter_by(name=subquantity['ingredient']).first()
        db.session.add(Subquantity(
            id_subrecipe=subrecipe_id,
            amount=subquantity['amount'],
            id_ingredient=ing.id,
            id_unit=subquantity['unit']
        ))
