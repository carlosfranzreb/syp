from flask_wtf import FlaskForm
from syp.seasons.utils import get_actual_season
from wtforms import SelectField, SubmitField


class SeasonForm(FlaskForm):
    seasons = [(1, 'Invierno'), (2, 'Primavera'), (3, 'Verano'), (4, 'Otoño')]
    season = SelectField('Escoge una temporada', choices=seasons,
                         default=get_actual_season())
    submit = SubmitField('Buscar')
