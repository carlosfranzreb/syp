from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from syp import db, bcrypt
from syp.models import User
from syp.users.forms import LoginForm
from syp.recipes.utils import get_last_recipes
from syp.search.forms import RecipesForm
import sys


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
            print(request.args.get('next'), file=sys.stdout)
            next = request.args.get('next')
            return redirect(next) if next else redirect(url_for('main.get_home'))
        else:
            flash('Email o contraseña incorrectos. Vuelve a intentarlo.', 'danger')
    return render_template('login.html',
                           title='Login',
                           form=form,
                           recipe_form=RecipesForm(),
                           last_recipes=get_last_recipes(4))
