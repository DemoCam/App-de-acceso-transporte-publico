from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, TimeField, IntegerField, FloatField, BooleanField, SubmitField, SelectField, PasswordField, EmailField
from wtforms.validators import DataRequired, Length, NumberRange, Optional, Email, EqualTo, ValidationError

class RutaForm(FlaskForm):
    """Formulario para crear y editar rutas"""
    numero = StringField('Número', validators=[DataRequired(), Length(max=10)], 
                        render_kw={"aria-label": "Número de ruta", "placeholder": "Ej: T31"})
    nombre = StringField('Nombre', validators=[DataRequired(), Length(max=100)], 
                        render_kw={"aria-label": "Nombre de la ruta", "placeholder": "Ej: Troncal Aguablanca"})
    origen = StringField('Origen', validators=[DataRequired(), Length(max=100)], 
                        render_kw={"aria-label": "Origen de la ruta", "placeholder": "Ej: Terminal Andrés Sanín"})
    destino = StringField('Destino', validators=[DataRequired(), Length(max=100)], 
                        render_kw={"aria-label": "Destino de la ruta", "placeholder": "Ej: Terminal Calipso"})
    hora_inicio = TimeField('Hora de inicio', validators=[DataRequired()], 
                          render_kw={"aria-label": "Hora de inicio de la ruta", "placeholder": "HH:MM"})
    hora_fin = TimeField('Hora de fin', validators=[DataRequired()], 
                       render_kw={"aria-label": "Hora de fin de la ruta", "placeholder": "HH:MM"})
    frecuencia_minutos = IntegerField('Frecuencia (minutos)', validators=[DataRequired(), NumberRange(min=1)], 
                                   render_kw={"aria-label": "Frecuencia en minutos", "placeholder": "Ej: 15"})
    descripcion = TextAreaField('Descripción', validators=[Optional(), Length(max=500)], 
                              render_kw={"aria-label": "Descripción de la ruta", 
                                       "placeholder": "Descripción detallada de la ruta para usuarios con discapacidad visual"})
    submit = SubmitField('Guardar', 
                       render_kw={"aria-label": "Guardar ruta"})

class ParadaForm(FlaskForm):
    """Formulario para crear y editar paradas"""
    nombre = StringField('Nombre', validators=[DataRequired(), Length(max=100)], 
                        render_kw={"aria-label": "Nombre de la parada", "placeholder": "Ej: Estación Unidad Deportiva"})
    direccion = StringField('Dirección', validators=[DataRequired(), Length(max=200)], 
                          render_kw={"aria-label": "Dirección de la parada", 
                                   "placeholder": "Ej: Calle 5 con Carrera 50"})
    latitud = FloatField('Latitud', validators=[DataRequired()], 
                       render_kw={"aria-label": "Latitud de la parada", "placeholder": "Ej: 3.4516"})
    longitud = FloatField('Longitud', validators=[DataRequired()], 
                        render_kw={"aria-label": "Longitud de la parada", "placeholder": "Ej: -76.5320"})
    tipo = SelectField('Tipo', validators=[DataRequired()], 
                     choices=[('regular', 'Parada Regular'), 
                             ('estacion', 'Estación'), 
                             ('terminal', 'Terminal')], 
                     render_kw={"aria-label": "Tipo de parada"})
    tiene_rampa = BooleanField('Tiene rampa', default=False, 
                             render_kw={"aria-label": "La parada tiene rampa de acceso"})
    tiene_semaforo_sonoro = BooleanField('Tiene semáforo sonoro', default=False, 
                                       render_kw={"aria-label": "La parada tiene semáforo sonoro"})
    descripcion = TextAreaField('Descripción', validators=[Optional(), Length(max=500)], 
                              render_kw={"aria-label": "Descripción de la parada", 
                                       "placeholder": "Descripción detallada de la parada para usuarios con discapacidad visual"})
    submit = SubmitField('Guardar', 
                       render_kw={"aria-label": "Guardar parada"})

class RutaParadaForm(FlaskForm):
    """Formulario para asignar paradas a rutas"""
    ruta_id = SelectField('Ruta', coerce=int, validators=[DataRequired()], 
                        render_kw={"aria-label": "Seleccione la ruta"})
    parada_id = SelectField('Parada', coerce=int, validators=[DataRequired()], 
                          render_kw={"aria-label": "Seleccione la parada"})
    orden = IntegerField('Orden', validators=[DataRequired(), NumberRange(min=1)], 
                       render_kw={"aria-label": "Orden de la parada en la ruta", "placeholder": "Ej: 1"})
    tiempo_estimado = IntegerField('Tiempo estimado (minutos)', validators=[Optional(), NumberRange(min=0)], 
                                render_kw={"aria-label": "Tiempo estimado en minutos desde el inicio de la ruta", 
                                         "placeholder": "Ej: 15"})
    submit = SubmitField('Asignar', 
                       render_kw={"aria-label": "Asignar parada a ruta"})

class UsuarioAdminForm(FlaskForm):
    """Formulario para crear y editar usuarios desde el panel de administración"""
    nombre_usuario = StringField('Nombre de usuario', validators=[DataRequired(), Length(min=3, max=50)],
                               render_kw={"aria-label": "Nombre de usuario", "placeholder": "Ej: juan.perez"})
    email = EmailField('Email', validators=[DataRequired(), Email()],
                     render_kw={"aria-label": "Email", "placeholder": "Ej: juan.perez@email.com"})
    password = PasswordField('Contraseña', validators=[Length(min=6)],
                           render_kw={"aria-label": "Contraseña"})
    confirm_password = PasswordField('Confirmar Contraseña', 
                                   validators=[EqualTo('password', message='Las contraseñas no coinciden')],
                                   render_kw={"aria-label": "Confirmar contraseña"})
    rol = SelectField('Rol', validators=[DataRequired()],
                    choices=[('usuario', 'Usuario Normal'), ('admin', 'Administrador')],
                    render_kw={"aria-label": "Rol del usuario"})
    submit = SubmitField('Guardar',
                       render_kw={"aria-label": "Guardar usuario"})

    def __init__(self, *args, **kwargs):
        self.instance = kwargs.pop('instance', None)
        super(UsuarioAdminForm, self).__init__(*args, **kwargs)
