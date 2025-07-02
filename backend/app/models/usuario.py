from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from enum import Enum
import datetime

class Role(str, Enum):
    ADMIN = 'admin'
    USER = 'user'
    GUEST = 'guest'

class Usuario(UserMixin, db.Model):
    """Modelo para los usuarios del sistema"""
    __tablename__ = 'usuarios'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    nombre = db.Column(db.String(64))
    apellido = db.Column(db.String(64))
    rol = db.Column(db.String(20), default=Role.USER)  # Cambiado de 'role' a 'rol' para coincidir con la BD
    fecha_ultimo_acceso = db.Column(db.DateTime, name='fecha_ultimo_acceso', default=datetime.datetime.utcnow)
    fecha_registro = db.Column(db.DateTime, name='fecha_registro', default=datetime.datetime.utcnow)
    activo = db.Column(db.Boolean, name='activo', default=True)
    
    def set_password(self, password):
        """Genera un hash seguro para la contraseña del usuario"""
        # Use a consistent method to avoid issues - pbkdf2:sha256 is more widely compatible
        self.password_hash = generate_password_hash(password, method='pbkdf2:sha256')
        print(f"Hash generado para {self.username}: {self.password_hash}")
    
    def check_password(self, password):
        """Verifica que la contraseña ingresada corresponda con el hash guardado"""
        result = check_password_hash(self.password_hash, password)
        print(f"Verificación de contraseña para {self.username}: {result}")
        return result
    
    def is_admin(self):
        """Verifica si el usuario tiene rol de administrador"""
        return self.rol == Role.ADMIN
        
    def get_full_name(self):
        """Retorna el nombre completo del usuario"""
        if self.nombre and self.apellido:
            return f"{self.nombre} {self.apellido}"
        elif self.nombre:
            return self.nombre
        else:
            return self.username
    
    @staticmethod
    def crear_admin_inicial(app):
        """Crea un usuario administrador si no existe ningún administrador en la base de datos"""
        with app.app_context():
            # Verificar si ya existe un usuario administrador
            admin = Usuario.query.filter_by(rol=Role.ADMIN).first()
            if not admin:
                # Usar valores del entorno o predeterminados para el usuario admin
                from flask import current_app
                import os
                
                admin_username = os.environ.get('ADMIN_USERNAME', 'admin')
                admin_password = os.environ.get('ADMIN_PASSWORD', 'admin2023')
                admin_email = os.environ.get('ADMIN_EMAIL', 'admin@transporte-accesible.com')
                
                admin = Usuario(
                    username=admin_username,
                    email=admin_email,
                    nombre="Administrador",
                    apellido="Sistema",
                    rol=Role.ADMIN,
                    activo=True
                )
                admin.set_password(admin_password)
                
                db.session.add(admin)
                db.session.commit()
                print(f"Usuario administrador creado: {admin_username}")
            else:
                print("Ya existe un usuario administrador")
    
    def __repr__(self):
        return f'<Usuario {self.username} ({self.rol})>'
