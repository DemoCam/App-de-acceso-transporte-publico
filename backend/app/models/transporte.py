from app import db
from datetime import datetime

class Ruta(db.Model):
    """Modelo para las rutas de transporte público"""
    __tablename__ = 'rutas'
    
    id = db.Column(db.Integer, primary_key=True)
    numero = db.Column(db.String(10), unique=True, nullable=False)
    nombre = db.Column(db.String(100), nullable=False)
    origen = db.Column(db.String(100), nullable=False)
    destino = db.Column(db.String(100), nullable=False)
    hora_inicio = db.Column(db.Time, nullable=False)
    hora_fin = db.Column(db.Time, nullable=False)
    frecuencia_minutos = db.Column(db.Integer, default=15)
    descripcion = db.Column(db.Text)
    activa = db.Column(db.Boolean, default=True)
    # Características de accesibilidad
    tiene_rampa = db.Column(db.Boolean, default=False)
    tiene_audio = db.Column(db.Boolean, default=False)
    tiene_espacio_silla = db.Column(db.Boolean, default=False)
    tiene_indicador_visual = db.Column(db.Boolean, default=False)
    
    # Relación con paradas a través de RutaParada
    paradas = db.relationship(
        'Parada',
        secondary='ruta_parada',
        backref=db.backref('rutas', lazy='dynamic'),
        lazy='dynamic',
        viewonly=True  # Usamos viewonly porque ahora gestionamos la relación a través de RutaParada
    )
    
    def __repr__(self):
        return f'<Ruta {self.numero}: {self.origen} - {self.destino}>'
    
    def to_dict(self, include_paradas=False):
        data = {
            'id': self.id,
            'numero': self.numero,
            'nombre': self.nombre,
            'origen': self.origen,
            'destino': self.destino,
            'hora_inicio': self.hora_inicio.strftime('%H:%M'),
            'hora_fin': self.hora_fin.strftime('%H:%M'),
            'frecuencia_minutos': self.frecuencia_minutos,
            'descripcion': self.descripcion,
            'activa': self.activa,
            'accesibilidad': {
                'tiene_rampa': self.tiene_rampa,
                'tiene_audio': self.tiene_audio,
                'tiene_espacio_silla': self.tiene_espacio_silla,
                'tiene_indicador_visual': self.tiene_indicador_visual
            }
        }
        
        if include_paradas:
            data['paradas'] = [parada.to_dict() for parada in self.paradas]
        
        return data
        
    @property
    def horario(self):
        """Devuelve una representación formateada del horario de la ruta"""
        return f"{self.hora_inicio.strftime('%H:%M')} - {self.hora_fin.strftime('%H:%M')}"

class Parada(db.Model):
    """Modelo para las paradas de transporte público"""
    __tablename__ = 'paradas'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    direccion = db.Column(db.String(200), nullable=False)
    latitud = db.Column(db.Float, nullable=False)
    longitud = db.Column(db.Float, nullable=False)
    tipo = db.Column(db.String(50), default='regular')  # regular, estación, terminal
    tiene_rampa = db.Column(db.Boolean, default=False)
    tiene_semaforo_sonoro = db.Column(db.Boolean, default=False)
    descripcion = db.Column(db.Text)
    
    def __repr__(self):
        return f'<Parada {self.nombre}: {self.direccion}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'direccion': self.direccion,
            'latitud': self.latitud,
            'longitud': self.longitud,
            'tipo': self.tipo,
            'accesibilidad': {
                'rampa': self.tiene_rampa,
                'semaforo_sonoro': self.tiene_semaforo_sonoro
            },
            'descripcion': self.descripcion
        }

# Modelo de asociación entre rutas y paradas
class RutaParada(db.Model):
    """Modelo para la relación entre rutas y paradas, con atributos adicionales"""
    __tablename__ = 'ruta_parada'
    
    # Clave primaria compuesta
    ruta_id = db.Column(db.Integer, db.ForeignKey('rutas.id'), primary_key=True)
    parada_id = db.Column(db.Integer, db.ForeignKey('paradas.id'), primary_key=True)
    orden = db.Column(db.Integer, nullable=False)
    tiempo_estimado = db.Column(db.Integer, nullable=True)  # Tiempo estimado en minutos desde origen
    
    # Relaciones para acceder fácilmente a los objetos relacionados
    ruta = db.relationship('Ruta', backref=db.backref('ruta_paradas', cascade='all, delete-orphan'))
    parada = db.relationship('Parada', backref=db.backref('ruta_paradas', cascade='all, delete-orphan'))
