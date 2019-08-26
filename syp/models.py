from syp import db


subrecipes = db.Table('t_subrecipes_in_recipe',
                      db.Column('id_recipe', db.Integer,
                                db.ForeignKey('t_recipes.id'),
                                primary_key=True),
                      db.Column('id_subrecipe', db.Integer,
                                db.ForeignKey('t_subrecipes.id'),
                                primary_key=True))


class Recipe(db.Model):
    __tablename__ = 't_recipes'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    time_prep = db.Column(db.Integer, nullable=False)
    time_cook = db.Column(db.Integer, nullable=False)
    intro = db.Column(db.Text, nullable=False)
    text = db.Column(db.Text, nullable=False)
    steps = db.Column(db.Text, nullable=False)
    link_video = db.Column(db.String(100), nullable=False)
    health = db.Column(db.Text, nullable=False)
    date_created = db.Column(db.DateTime, nullable=False)
    id_season = db.Column(db.Integer, db.ForeignKey('t_seasons.id'),
                          nullable=False)
    subrecipes = db.relationship('Subrecipe', secondary=subrecipes, lazy=True,
                                 backref=db.backref('recipes', lazy=True))

    def __repr__(self):
        return f"Recipe('{self.name}', '{self.intro}')"


class Subrecipe(db.Model):
    __tablename__ = 't_subrecipes'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    steps = db.Column(db.Text, nullable=False)
    date_created = db.Column(db.DateTime, nullable=False)
    case_fem = db.Column(db.Boolean, nullable=False)  # 0=masc., 1=fem.

    def __repr__(self):
        return f"Subrecipe('{self.name}')"


class Season(db.Model):
    __tablename__ = 't_seasons'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(10), nullable=False)
    recipes = db.relationship('Recipe', backref='season', lazy=True)

    def __repr__(self):
        return f"Season('{self.name}', '{self.recipes}')"


class Ingredient(db.Model):
    __tablename__ = 't_ingredients'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    health = db.Column(db.Text, nullable=False)
    id_unit = db.Column(db.Integer, db.ForeignKey('t_units.id'),
                        nullable=False)
    id_group = db.Column(db.Integer, db.ForeignKey('t_ingredient_groups.id'),
                         nullable=False)

    def __repr__(self):
        return f"Ingredient('{self.name}')"


class Unit(db.Model):
    __tablename__ = 't_units'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(10), nullable=False)
    ingredients = db.relationship('Ingredient', backref='unit', lazy=True)

    def __repr__(self):
        return f"Unit('{self.name}', '{self.ingredients}')"


class Ingredient_group(db.Model):
    __tablename__ = 't_ingredient_groups'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    ingredients = db.relationship('Ingredient', backref='group', lazy=True)

    def __repr__(self):
        return f"Ingredient group('{self.name}', '{self.ingredients}')"


class Quantity(db.Model):
    __tablename__ = 't_ingredients_in_recipe'
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Integer, nullable=False)
    id_recipe = db.Column(db.Integer, db.ForeignKey('t_recipes.id'),
                          nullable=False)
    id_ingredient = db.Column(db.Integer, db.ForeignKey('t_ingredients.id'),
                              nullable=False)


class Subquantity(db.Model):
    __tablename__ = 't_ingredients_in_subrecipe'
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Integer, nullable=False)
    id_subrecipe = db.Column(db.Integer, db.ForeignKey('t_subrecipes.id'),
                             nullable=False)
    id_ingredient = db.Column(db.Integer, db.ForeignKey('t_ingredients.id'),
                              nullable=False)


class Ingredient_season(db.Model):
    __tablename__ = 't_seasons_for_ingredient'
    id = db.Column(db.Integer, primary_key=True)
    id_season = db.Column(db.Integer, db.ForeignKey('t_seasons.id'),
                          nullable=False)
    id_ingredient = db.Column(db.Integer, db.ForeignKey('t_ingredients.id'),
                              nullable=False)

    def __repr__(self):
        return f"Ingredient season('{self.id_ingredient}')"


class User(db.Model):
    __tablename__ = 't_users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    pw = db.Column(db.String(60), nullable=False)
    birth_date =  db.Column(db.DateTime, nullable=False)
    id_city = db.Column(db.Integer, db.ForeignKey('t_cities.id'),
                        nullable=False)
    id_role = db.Column(db.Integer, db.ForeignKey('t_roles.id'),
                        nullable=False)

    def __repr__(self):
        return f"User '{self.username}' from {self.city}"


class Role(db.Model):
    __tablename__ = 't_roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    description = db.Column(db.Text, unique=True, nullable=False)
    users = db.relationship('User', backref='role', lazy=True)

    def __repr__(self):
        return f"Ingredient season('{self.id_ingredient}')"


class City(db.Model):
    __tablename__ = 't_cities'
    id = db.Column(db.Integer, primary_key=True)
    country = db.Column(db.String(200), nullable=False)
    city = db.Column(db.String(200), unique=True, nullable=False)
    latitude = db.Column(db.Float((10, 8)), nullable=False)
    longitude = db.Column(db.Float((11, 8)), nullable=False)
    users = db.relationship('User', backref='city', lazy=True)

    def __repr__(self):
        return f"Ingredient season('{self.id_ingredient}')"
