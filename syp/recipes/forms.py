from flask_wtf import FlaskForm, RecaptchaField
from wtforms import (Form, StringField, SubmitField, BooleanField,
                     SelectMultipleField, IntegerField, SelectField,
                     FieldList, FormField, TextAreaField, FloatField)
from wtforms.validators import DataRequired, InputRequired, Length
from flask_wtf.file import FileField, FileAllowed


class StepForm(Form):
    step = TextAreaField('Paso:', validators=[DataRequired()])


class IngredientForm(Form):
    ingredient = StringField('Ingrediente:', validators=[DataRequired()])
    amount = FloatField('Cantidad:', validators=[InputRequired()])
    unit = SelectField('Unidad:', validators=[InputRequired()], coerce=int)


class SubrecipeForm(Form):
    subrecipe = StringField('Subreceta:', validators=[DataRequired()])


class RecipeForm(FlaskForm):
    name = StringField('Nombre de la receta.',
                              validators=[DataRequired(), Length(max=100)])
    image = FileField('Foto del plato.', validators=[FileAllowed(['jpg', 'png'])])
    time_prep = IntegerField('Tiempo de preparación.', validators=[DataRequired()])
    time_cook = IntegerField('Tiempo de preparación.', validators=[DataRequired()])
    season = SelectField('Temporada.', coerce=int)
    intro = TextAreaField('Un par de frases para promocionar la receta.',
                          validators=[DataRequired(), Length(min=80, max=180)])
    text = TextAreaField('Explicación detallada de la receta.',
                         validators=[DataRequired(), Length(min=600, max=1400)])
    steps = FieldList(FormField(StepForm), min_entries=1)
    ingredients = FieldList(FormField(IngredientForm), min_entries=1)
    subrecipes = FieldList(FormField(SubrecipeForm))
    health = TextAreaField('Descripción de los nutrientes de la receta.',
                         validators=[DataRequired(), Length(min=300, max=600)])
    link_video = StringField('Link del vídeo de YouTube.')
    save = SubmitField('Guardar')
