from flask import Blueprint, flash, redirect, render_template, url_for
from syp.recipes.utils import get_last_recipes
from syp.search.forms import RecipesForm
from syp.veganizer.forms import VeggieForm
from syp.veganizer.utils import send_veggie_msg, get_veggie_keywords


veganizer = Blueprint('veganizer', __name__)


@veganizer.route('/veganizador', methods=['GET', 'POST'])
def get_veganizer():
    form = VeggieForm()
    if form.validate_on_submit():
        flash(f'Gracias {form.name.data}! Te mandaremos un email cuando \
                la receta esté online', 'success')
        send_veggie_msg(form)
        return redirect(url_for('main.get_home'))

    desc = "Envíanos tus recetas favoritas, y nosotros idearemos versiones \
            veganas y saludables, para que tu paladar mantenga el listón y \
            las viejas costumbres no desaparezcan"
    return render_template('veganizer.html',
                           title='Veganizador',
                           recipe_form=RecipesForm(),
                           form=form,
                           last_recipes=get_last_recipes(4),
                           description=' '.join(desc.split()),
                           keywords=get_veggie_keywords())
