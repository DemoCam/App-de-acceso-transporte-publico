"""
Script simplificado para ejecutar la aplicación Flask directamente
sin depender de variables de entorno.
"""
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Importar la aplicación
from app import create_app

app = create_app()

if __name__ == '__main__':
    # Imprimir información útil
    print("Iniciando la aplicación...")
    print(f"URL de base de datos: {app.config.get('SQLALCHEMY_DATABASE_URI', 'No configurada')}")
    print(f"Blueprints registrados: {[bp.name for bp in app.blueprints.values()]}")
    print(f"Rutas disponibles:")
    for rule in app.url_map.iter_rules():
        print(f"  {rule.endpoint} -> {rule.rule}")
    
    # Ejecutar la aplicación
    app.run(debug=True, port=5000)
