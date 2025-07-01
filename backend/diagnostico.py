"""
Script de diagnóstico completo para la aplicación
"""
import os
import sys
import subprocess
import importlib
import pkgutil

def check_python_version():
    """Verifica la versión de Python"""
    print(f"Python versión: {sys.version}")
    if sys.version_info < (3, 8):
        print("⚠️ ADVERTENCIA: Se recomienda Python 3.8 o superior")
    else:
        print("✅ Versión de Python OK")

def check_package_installation(package_name):
    """Verifica si un paquete está instalado y su versión"""
    try:
        pkg = importlib.import_module(package_name)
        version = getattr(pkg, '__version__', 'Desconocida')
        print(f"✅ {package_name} está instalado (versión: {version})")
        return True
    except ImportError:
        print(f"❌ {package_name} no está instalado")
        return False
    except Exception as e:
        print(f"❌ Error al importar {package_name}: {e}")
        return False

def check_sqlalchemy():
    """Verifica la instalación de SQLAlchemy específicamente"""
    print("\n--- Diagnóstico de SQLAlchemy ---")
    try:
        import sqlalchemy
        print(f"✅ SQLAlchemy está instalado (versión: {sqlalchemy.__version__})")
        
        # Probar acceso a atributos importantes
        print("Probando acceso a atributos de SQLAlchemy...")
        try:
            print(f"  - Column: {sqlalchemy.Column}")
            print(f"  - String: {sqlalchemy.String}")
            print(f"  - Integer: {sqlalchemy.Integer}")
            print("✅ Acceso a atributos de SQLAlchemy OK")
        except AttributeError as e:
            print(f"❌ Error al acceder a atributos de SQLAlchemy: {e}")
            print("⚠️ Posible instalación corrupta o conflicto de versiones")
            
        return True
    except ImportError:
        print(f"❌ SQLAlchemy no está instalado")
        return False
    except Exception as e:
        print(f"❌ Error al importar SQLAlchemy: {e}")
        print("⚠️ Este error sugiere una instalación corrupta o un conflicto de versiones")
        return False

def check_flask_sqlalchemy():
    """Verifica la instalación de Flask-SQLAlchemy específicamente"""
    print("\n--- Diagnóstico de Flask-SQLAlchemy ---")
    try:
        import flask_sqlalchemy
        print(f"✅ Flask-SQLAlchemy está instalado")
        
        # Probar acceso a clases importantes
        print("Probando acceso a clases de Flask-SQLAlchemy...")
        try:
            print(f"  - SQLAlchemy class: {flask_sqlalchemy.SQLAlchemy}")
            print("✅ Acceso a clases de Flask-SQLAlchemy OK")
        except AttributeError as e:
            print(f"❌ Error al acceder a clases de Flask-SQLAlchemy: {e}")
            print("⚠️ Posible instalación corrupta o conflicto de versiones")
            
        return True
    except ImportError:
        print(f"❌ Flask-SQLAlchemy no está instalado")
        return False
    except Exception as e:
        print(f"❌ Error al importar Flask-SQLAlchemy: {e}")
        print("⚠️ Este error sugiere una instalación corrupta o un conflicto de versiones")
        return False

def check_installed_packages():
    """Muestra los paquetes instalados en el entorno"""
    print("\n--- Paquetes instalados ---")
    result = subprocess.run("pip list", shell=True, text=True, capture_output=True)
    print(result.stdout)

def check_env_file():
    """Verifica si existe el archivo .env y muestra su contenido"""
    print("\n--- Verificando archivo .env ---")
    env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.env')
    
    if os.path.exists(env_path):
        print(f"✅ Archivo .env encontrado")
        print("Contenido (sin contraseñas):")
        with open(env_path, 'r') as f:
            for line in f:
                # No mostrar contraseñas u otra información sensible
                if 'PASSWORD' in line or 'SECRET' in line:
                    parts = line.split('=', 1)
                    if len(parts) == 2:
                        print(f"{parts[0]}=[OCULTA]")
                else:
                    print(line.strip())
    else:
        print(f"❌ Archivo .env no encontrado")
        print("⚠️ La aplicación puede tener problemas para configurar la base de datos")

def check_project_structure():
    """Verifica la estructura del proyecto"""
    print("\n--- Verificando estructura del proyecto ---")
    current_dir = os.path.dirname(os.path.abspath(__file__))
    app_dir = os.path.join(current_dir, 'app')
    
    if os.path.exists(app_dir):
        print(f"✅ Directorio app/ encontrado")
        # Verificar subdirectorios importantes
        for subdir in ['routes', 'models', 'templates', 'static']:
            path = os.path.join(app_dir, subdir)
            if os.path.exists(path):
                print(f"✅ Directorio app/{subdir}/ encontrado")
            else:
                print(f"❌ Directorio app/{subdir}/ no encontrado")
    else:
        print(f"❌ Directorio app/ no encontrado")
        print("⚠️ La estructura del proyecto parece estar dañada")

def main():
    """Función principal del script de diagnóstico"""
    print("===== DIAGNÓSTICO DE LA APLICACIÓN =====\n")
    
    print("--- Información del sistema ---")
    check_python_version()
    print(f"Sistema operativo: {sys.platform}")
    
    print("\n--- Verificando dependencias principales ---")
    packages = ['flask', 'sqlalchemy', 'flask_sqlalchemy', 'mysql.connector', 'dotenv']
    for package in packages:
        check_package_installation(package)
    
    # Verificaciones específicas
    check_sqlalchemy()
    check_flask_sqlalchemy()
    
    # Verificar estructura del proyecto
    check_project_structure()
    
    # Verificar archivo .env
    check_env_file()
    
    # Mostrar paquetes instalados
    check_installed_packages()
    
    print("\n===== FIN DEL DIAGNÓSTICO =====")
    print("\nSi encontraste errores relacionados con SQLAlchemy, ejecuta:")
    print("python fix_sqlalchemy.py")
    print("\nSi quieres probar una versión mínima de la aplicación sin SQLAlchemy, ejecuta:")
    print("python app_minimal.py")
    
if __name__ == "__main__":
    main()
    input("\nPresiona Enter para salir...")
