import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

# Carga las variables de entorno desde el archivo .env
load_dotenv()

# Inicializa las extensiones
db = SQLAlchemy()

# Bootstrap será inicializado después de importar Flask

def create_app():
    """Función factory para crear la aplicación Flask"""
    
    # Crear instancia de Flask
    app = Flask(__name__)
    
    # Configuración de la aplicación
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'clave-predeterminada-cambiar')
    
    # Conexión a MySQL (compatible con XAMPP)
    db_user = os.environ.get('DATABASE_USER', 'root')
    db_password = os.environ.get('DATABASE_PASSWORD', '')
    db_host = os.environ.get('DATABASE_HOST', 'localhost')
    db_name = os.environ.get('DATABASE_NAME', 'transporte_accesible_cali')
    
    # Crear URI de conexión segura que maneje contraseñas vacías
    if db_password:
        app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql://{db_user}:{db_password}@{db_host}/{db_name}"
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql://{db_user}@{db_host}/{db_name}"
        
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Inicializar extensiones con la aplicación
    db.init_app(app)
    
    # Importamos Bootstrap solo si está instalado
    try:
        from flask_bootstrap import Bootstrap
        bootstrap = Bootstrap()
        bootstrap.init_app(app)
    except ImportError:
        print("Flask-Bootstrap no está instalado. La UI puede no verse correctamente.")
    
    # Registro de blueprints (rutas)
    try:
        from app.routes.main import main as main_blueprint
        app.register_blueprint(main_blueprint)
        print("Blueprint 'main' registrado correctamente")
        
        from app.routes.api import api as api_blueprint
        app.register_blueprint(api_blueprint, url_prefix='/api')
        print("Blueprint 'api' registrado correctamente")
    except ImportError as e:
        print(f"Error al importar los blueprints principales: {e}")
        print("Utilizando blueprints simplificados como alternativa...")
        try:
            from app.routes.main_simple import register_simple_routes
            register_simple_routes(app)
        except ImportError:
            print("Error: No se pudo cargar ni siquiera los blueprints simplificados")
    
    # Crear tablas de la base de datos si no existen
    try:
        with app.app_context():
            db.create_all()
            print("Tablas de la base de datos creadas correctamente")
    except Exception as e:
        print(f"Error al crear tablas de la base de datos: {e}")
    
    return app
