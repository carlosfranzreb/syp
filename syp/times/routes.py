from flask import Blueprint, flash, redirect, render_template, url_for
from syp.recipes.utils import get_last_recipes
from syp.search.forms import SearchRecipeForm
from syp.times.utils import get_recipes_by_time, get_times_keywords
from syp.times.forms import TimesForm


times = Blueprint('times', __name__)


@times.route('/tiempo', methods=['GET', 'POST'])
def search_time_undefined():
    form = TimesForm()
    if form.is_submitted():
        return redirect(url_for('times.search_time', time=form.time.data))

    desc = 'Busca recetas veganas y saludables por tiempo; por si tienes \
            prisa, o buscas un plato más elaborado. Sin importar lo que \
            tardes, ¡dedícale tiempo a degustarlo!'
    return render_template(
        'time.html',
        title='Tiempo',
        recipe_form=SearchRecipeForm(),
        form=form,
        recipes=None,
        last_recipes=get_last_recipes(4),
        description=' '.join(desc.split()),
        keywords=get_times_keywords()
    )


@times.route('/tiempo/<time>minutos', methods=['GET', 'POST'])
def search_time(time):
    form = TimesForm()
    if form.is_submitted():
        return redirect(url_for('times.search_time', time=form.time.data))
    page, recs = get_recipes_by_time(time)
    if isinstance(recs, str):
        flash(recs, 'danger')
        return redirect(url_for('times.search_time_undefined'))
    desc = f'Busca recetas veganas y saludables hechas en menos de {time} \
             minutos. Sin importar lo que tardes, ¡dedícale tiempo a \
             degustarlo!'
    return render_template(
        'time.html',
        title=f'{time} minutos',
        recipe_form=SearchRecipeForm(),
        form=form,
        recipes=recs,
        time=time,
        last_recipes=get_last_recipes(4),
        description=' '.join(desc.split()),
        keywords=get_times_keywords(time)
    )
