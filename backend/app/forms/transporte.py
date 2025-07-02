from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, TimeField, IntegerField, SelectField, BooleanField, SubmitField, FloatField
from wtforms.validators import DataRequired, Length, NumberRange, Optional

class RutaForm(FlaskForm):
    """Formulario para gestionar rutas de transporte"""
    numero = StringField('Número de Ruta', validators=[
        DataRequired(),
        Length(min=1, max=10)
    ])
    nombre = StringField('Nombre de la Ruta', validators=[
        DataRequired(),
        Length(min=3, max=100)
    ])
    origen = StringField('Origen', validators=[
        DataRequired(),
        Length(min=3, max=100)
    ])
    destino = StringField('Destino', validators=[
        DataRequired(),
        Length(min=3, max=100)
    ])
    hora_inicio = TimeField('Hora de Inicio', format='%H:%M', validators=[
        DataRequired()
    ])
    hora_fin = TimeField('Hora de Finalización', format='%H:%M', validators=[
        DataRequired()
    ])
    frecuencia_minutos = IntegerField('Frecuencia (minutos)', validators=[
        DataRequired(),
        NumberRange(min=1, max=180)
    ])
    descripcion = TextAreaField('Descripción', validators=[
        Optional(),
        Length(max=500)
    ])
    activa = BooleanField('Ruta Activa', default=True)
    # Características de accesibilidad
    tiene_rampa = BooleanField('Vehículos con rampa de acceso')
    tiene_audio = BooleanField('Anuncios de audio')
    tiene_espacio_silla = BooleanField('Espacio para silla de ruedas')
    tiene_indicador_visual = BooleanField('Indicadores visuales')
    submit = SubmitField('Guardar')

class ParadaForm(FlaskForm):
    """Formulario para gestionar paradas de transporte"""
    nombre = StringField('Nombre de la Parada', validators=[
        DataRequired(),
        Length(min=3, max=100)
    ])
    direccion = StringField('Dirección', validators=[
        DataRequired(),
        Length(min=3, max=200)
    ])
    latitud = FloatField('Latitud', validators=[
        DataRequired(),
        NumberRange(min=-90, max=90)
    ])
    longitud = FloatField('Longitud', validators=[
        DataRequired(),
        NumberRange(min=-180, max=180)
    ])
    tipo = SelectField('Tipo de Parada', choices=[
        ('regular', 'Parada Regular'),
        ('estacion', 'Estación'),
        ('terminal', 'Terminal')
    ], validators=[DataRequired()])
    tiene_rampa = BooleanField('Tiene Rampa')
    tiene_semaforo_sonoro = BooleanField('Tiene Semáforo Sonoro')
    descripcion = TextAreaField('Descripción', validators=[
        Optional(),
        Length(max=500)
    ])
    submit = SubmitField('Guardar')

class RutaParadaForm(FlaskForm):
    """Formulario para gestionar asociaciones entre rutas y paradas"""
    ruta_id = SelectField('Ruta', coerce=int, validators=[
        DataRequired()
    ])
    parada_id = SelectField('Parada', coerce=int, validators=[
        DataRequired()
    ])
    orden = IntegerField('Orden en la Ruta', validators=[
        DataRequired(),
        NumberRange(min=1)
    ])
    tiempo_estimado = IntegerField('Tiempo Estimado (minutos desde origen)', validators=[
        Optional(),
        NumberRange(min=0)
    ])
    submit = SubmitField('Guardar')
