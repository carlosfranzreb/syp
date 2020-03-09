from flask import Blueprint, render_template
from flask_login import login_required

from syp.subrecipes import utils
from syp.search.forms import SearchRecipeForm
from syp.recipes.utils import get_last_recipes
from syp.recipes.forms import SubrecipeForm


subrecipes = Blueprint('subrecipes', __name__)


@subrecipes.route('/subrecetas')
@login_required
def overview():
    return render_template(
        'subrecipes.html',
        recipe_form=SearchRecipeForm(),
        last_recipes=get_last_recipes(4),
        subrecipes=utils.get_paginated_subrecipes()[1]
    )