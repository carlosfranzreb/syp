""" Pages related to the administration of users. """
#pylint: disable = missing-function-docstring, invalid-name


from flask import render_template, url_for, flash, redirect, Blueprint, abort
from flask_login import login_user, current_user, logout_user, login_required

from syp import bcrypt
from syp.models.user import User
from syp.users.forms import LoginForm, ProfileForm, CookForm
from syp.recipes.utils import get_last_recipes
from syp.search.forms import SearchRecipeForm
from syp.users import utils, update, validate


users = Blueprint('users', __name__)


@users.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.get_home'))
    form = LoginForm()
    url = utils.get_url()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None:
            flash('El email no es correcto. Vuelve a intentarlo.', 'danger')
        elif user and bcrypt.check_password_hash(user.pw, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url)
        flash('La contraseña es incorrecta. Vuelve a intentarlo.', 'danger')
    return render_template(
        'view_login.html',
        title='Login',
        form=form,
        recipe_form=SearchRecipeForm(),
        last_recipes=get_last_recipes(4),
        url=url
    )


@users.route('/logout')
def logout():
    """ Logout and return to previous page. If the page requires a login,
    a 404 error will be thrown. """
    logout_user()
    return redirect(utils.get_url())


@users.route('/editar_perfil', methods=['GET', 'POST'])
@login_required
def edit_profile():
    """ Edit profile of the cook. """
    form = utils.add_choices(ProfileForm(obj=current_user), current_user)
    if form.validate_on_submit():
        errors = validate.validate_user(form, current_user)
        if len(errors) == 0:
            update.update_user(current_user, form)
            flash('Los cambios han sido guardados', 'success')
        else:
            for error in errors:
                flash(error, 'danger')
    return render_template(
        'edit_profile.html',
        title='Editar perfil',
        form=form,
        all_media=utils.all_media(),
        recipe_form=SearchRecipeForm(),
        last_recipes=get_last_recipes(4),
    )


@users.route('/<username>')
def view_profile(username):
    """ Returns the user home page, with an intro and recipes. """
    user = utils.get_user(username)
    if user is None:
        return abort(404)
    return render_template(
        'view_profile.html',
        title=username,
        user=user,
        user_recipes=utils.last_user_recipes(user.id),
        recipe_form=SearchRecipeForm(),
        last_recipes=get_last_recipes(4),
    )


@users.route('/cocineros', methods=['GET', 'POST'])
def all_cooks():
    form = CookForm()
    if form.is_submitted():
        return redirect(url_for(
            'users.search_cook',
            username=form.username.data
        ))
    page, cooks = utils.paginated_cooks()
    desc = 'Todas nuestras recetas, veganas y saludables. Aquí encontrarás \
    platos muy variados, algunas rápidas, otras más elaboradas, pero todas \
    bien explicadas y con vídeo incluido.'
    return render_template(
        'search_cooks.html',
        title='Cocineros',
        cook_form=form,
        all_usernames=utils.all_usernames(),
        cooks=cooks,
        recipe_form=SearchRecipeForm(),
        last_recipes=get_last_recipes(4),
        description=' '.join(desc.split()),
        keywords=utils.get_cook_keywords()
    )


@users.route('/cocineros/<username>', methods=['GET', 'POST'])
def search_cook(username):
    form = CookForm()
    if form.is_submitted():
        return redirect(url_for(
            'search.search_recipe',
            recipe_name=form.recipe.data
        ))
    page, cooks = utils.get_cooks(username)
    if isinstance(cooks, str):
        flash(cooks, 'danger')
        return redirect(url_for('utils.all_cooks'))
    return render_template(
        'search_cooks.html',
        title=username,
        cook_form=form,
        all_usernames=utils.all_usernames(),
        cooks=cooks,
        recipe_form=SearchRecipeForm(),
        last_recipes=get_last_recipes(),
        keywords=utils.get_cook_keywords(username)
    )
