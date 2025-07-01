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
    
    # Relación con paradas (muchos a muchos)
    paradas = db.relationship('Parada', 
                             secondary='ruta_parada',
                             backref=db.backref('rutas', lazy='dynamic'),
                             lazy='dynamic')
    
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
            'descripcion': self.descripcion
        }
        
        if include_paradas:
            data['paradas'] = [parada.to_dict() for parada in self.paradas]
        
        return data

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

# Tabla de relación muchos a muchos entre rutas y paradas
ruta_parada = db.Table('ruta_parada',
    db.Column('ruta_id', db.Integer, db.ForeignKey('rutas.id'), primary_key=True),
    db.Column('parada_id', db.Integer, db.ForeignKey('paradas.id'), primary_key=True),
    db.Column('orden', db.Integer, nullable=False),
    db.Column('tiempo_estimado', db.Integer, nullable=True)  # Tiempo estimado en minutos desde origen
)
