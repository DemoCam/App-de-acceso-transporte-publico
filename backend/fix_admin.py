"""
Script para corregir la aplicación y crear un nuevo administrador con una contraseña conocida
"""
import os
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash
from app import create_app, db
from app.models.usuario import Usuario

# Cargar variables de entorno
load_dotenv()

# Asegurar que la aplicación usa una clave secreta fija
def fix_app():
    """Corrige la configuración de la aplicación para que use una clave secreta fija"""
    # Asegurar que existe una clave secreta en el entorno
    if not os.environ.get('SECRET_KEY'):
        secret_key = os.urandom(32).hex()
        print(f"Generando una nueva clave secreta: {secret_key}")
        
        # Escribir la clave secreta al archivo .env
        env_path = os.path.join(os.path.dirname(__file__), '../.env')
        if not os.path.exists(os.path.dirname(env_path)):
            env_path = os.path.join(os.path.dirname(__file__), '.env')
        
        has_env = os.path.exists(env_path)
        
        with open(env_path, 'a' if has_env else 'w') as f:
            if has_env:
                f.write('\n')
            f.write(f'SECRET_KEY={secret_key}\n')
        
        os.environ['SECRET_KEY'] = secret_key
        print(f"Clave secreta guardada en {env_path}")
    
    # Crear la aplicación con la clave secreta del entorno
    return create_app()

# Crear un usuario administrador
def create_admin(app, username, password):
    """Crea un usuario administrador"""
    with app.app_context():
        # Verificar si el usuario ya existe
        usuario = Usuario.query.filter_by(username=username).first()
        if usuario:
            # Actualizar la contraseña
            usuario.password_hash = generate_password_hash(password)
            db.session.commit()
            print(f"Contraseña actualizada para el usuario '{username}'")
        else:
            # Crear el usuario
            nuevo_usuario = Usuario(
                username=username,
                email=f"{username}@transporte-cali.com",
                nombre="Admin",
                apellido="Sistema",
                rol="admin",
                activo=True
            )
            nuevo_usuario.password_hash = generate_password_hash(password)
            db.session.add(nuevo_usuario)
            db.session.commit()
            print(f"Usuario '{username}' creado correctamente")
        
        # Verificar que la contraseña se haya establecido correctamente
        usuario = Usuario.query.filter_by(username=username).first()
        if usuario.check_password(password):
            print(f"✅ Verificación exitosa: La contraseña se estableció correctamente")
        else:
            print(f"❌ Error: La contraseña no se estableció correctamente")
            print(f"Hash almacenado: {usuario.password_hash}")

if __name__ == "__main__":
    app = fix_app()
    create_admin(app, "adminfix", "Admin2025!")
