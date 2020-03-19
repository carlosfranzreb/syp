from flask import Flask
from flask_bcrypt import Bcrypt
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from syp.config import Config
from flask_login import LoginManager


db = SQLAlchemy()
mail = Mail()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    mail.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)


    from syp.main.routes import main
    from syp.users.routes import users
    from syp.ingredients.routes import ingredients
    from syp.recipes.routes import recipes
    from syp.search.routes import search
    from syp.seasons.routes import seasons
    from syp.subrecipes.routes import subrecipes
    from syp.times.routes import times
    from syp.veganizer.routes import veganizer
    from syp.errors.handlers import errors
    app.register_blueprint(main)
    app.register_blueprint(users)
    app.register_blueprint(ingredients)
    app.register_blueprint(recipes)
    app.register_blueprint(search)
    app.register_blueprint(seasons)
    app.register_blueprint(subrecipes)
    app.register_blueprint(times)
    app.register_blueprint(veganizer)
    app.register_blueprint(errors)

    return app
