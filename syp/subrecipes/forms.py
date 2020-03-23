from flask_wtf import FlaskForm
from wtforms import (
    Form,
    StringField,
    SubmitField,
    SelectField,
    FieldList,
    FormField,
    TextAreaField,
    FloatField,
)
from wtforms.validators import DataRequired, Length


class StepForm(Form):
    step = TextAreaField("Paso:", validators=[DataRequired(), Length(max=200)])


class IngredientForm(Form):
    ingredient = StringField("Ingrediente:")  # checked manually.
    amount = FloatField("Cantidad:", validators=[DataRequired()])
    unit = SelectField("Unidad:", coerce=int)  # an option is always chosen.


class SubrecipeForm(FlaskForm):
    name = StringField(
        "Nombre de la receta.", validators=[DataRequired(), Length(max=100)]
    )
    steps = FieldList(FormField(StepForm), min_entries=1)
    ingredients = FieldList(FormField(IngredientForm), min_entries=1)
    case = SelectField("Artículo:", coerce=int)
    save = SubmitField("Guardar")
