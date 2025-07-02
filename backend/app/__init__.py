import os
import secrets
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from dotenv import load_dotenv

# Carga las variables de entorno desde el archivo .env
load_dotenv()

# Usar una clave secreta del entorno o generar una fija para la sesión actual
SECRET_KEY = os.environ.get('SECRET_KEY')
if not SECRET_KEY:
    SECRET_KEY = '6c05d2a9a696a499afb43ed9dfd5c4c6ea1d8a7c62f5090b43bc5fc652a8697a'
    print(f"ADVERTENCIA: Usando clave secreta fija. Se recomienda configurar SECRET_KEY en .env")

# Inicializa las extensiones
db = SQLAlchemy()
login_manager = LoginManager()
csrf = CSRFProtect()

# Bootstrap será inicializado después de importar Flask

def create_app():
    """Función factory para crear la aplicación Flask"""
    
    # Crear instancia de Flask con rutas explícitas para plantillas y archivos estáticos
    import os
    from pathlib import Path
    
    # Obtener la ruta absoluta del directorio actual (donde está __init__.py)
    current_dir = Path(os.path.dirname(os.path.abspath(__file__)))
    template_dir = os.path.join(current_dir, 'templates')
    static_dir = os.path.join(current_dir, 'static')
    
    # Verificar si las carpetas existen
    print(f"Directorio de plantillas: {template_dir} {'(existe)' if os.path.exists(template_dir) else '(no existe)'}")
    print(f"Directorio estático: {static_dir} {'(existe)' if os.path.exists(static_dir) else '(no existe)'}")
    
    app = Flask(__name__, 
                template_folder=template_dir,
                static_folder=static_dir)
    
    # Configuración de la aplicación - Usar la clave secreta global definida arriba
    app.config['SECRET_KEY'] = SECRET_KEY
    print(f"Usando clave secreta: {SECRET_KEY[:10]}...")
    
    # Conexión a MySQL (compatible con XAMPP)
    db_user = os.environ.get('DATABASE_USER', 'root')
    db_password = os.environ.get('DATABASE_PASSWORD', '')
    db_host = os.environ.get('DATABASE_HOST', 'localhost')
    db_name = os.environ.get('DATABASE_NAME', 'transporte_accesible_cali')
    
    # Crear URI de conexión segura que maneje contraseñas vacías
    if db_password:
        app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_name}"
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{db_user}@{db_host}/{db_name}"
        
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Inicializar extensiones con la aplicación
    db.init_app(app)
    csrf.init_app(app)  # Inicializar CSRF protection
    
    # Asegurarnos que Flask-Login se inicialice después de configurar la clave secreta
    with app.app_context():
        # Configurar Flask-Login
        login_manager.init_app(app)
        login_manager.login_view = 'auth.login'
        login_manager.login_message = 'Por favor inicia sesión para acceder a esta página.'
        login_manager.login_message_category = 'info'
        
        # Configurar la función de carga de usuarios
        @login_manager.user_loader
        def load_user(user_id):
            from app.models.usuario import Usuario
            return Usuario.query.get(int(user_id))
    
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
        from app.routes.auth import auth as auth_blueprint
        from app.routes.admin import admin as admin_blueprint
        app.register_blueprint(main_blueprint)
        app.register_blueprint(auth_blueprint)
        app.register_blueprint(admin_blueprint)
        print("Blueprints 'main', 'auth' y 'admin' registrados correctamente")
        
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
            # Primero, nos aseguramos de que todas las tablas estén creadas.
            db.create_all()
            
            # Ahora que las tablas existen, podemos operar sobre ellas.
            from app.models.usuario import Usuario
            Usuario.crear_admin_inicial(app)
            print("Inicialización de la base de datos completada.")
    except Exception as e:
        print(f"Error durante la inicialización de la base de datos: {e}")
    
    return app
