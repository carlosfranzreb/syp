""" Pages related to the administration of users. """
#pylint: disable = missing-function-docstring, invalid-name


from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user

from syp import bcrypt
from syp.models.user import User
from syp.users.forms import LoginForm
from syp.recipes.utils import get_last_recipes
from syp.search.forms import SearchRecipeForm


users = Blueprint('users', __name__)


@users.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.get_home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.pw, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')  # TODO: not returning to the prev. page.
            return redirect(next_page) if next_page else redirect(url_for('main.get_home'))
        flash('Email o contraseña incorrectos. Vuelve a intentarlo.', 'danger')
    return render_template('login.html',
                           title='Login',
                           form=form,
                           recipe_form=SearchRecipeForm(),
                           last_recipes=get_last_recipes(4))
