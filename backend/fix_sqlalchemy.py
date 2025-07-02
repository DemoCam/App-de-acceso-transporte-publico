"""
Script para arreglar la estructura de la base de datos después de cambios en los modelos.
Útil cuando aparecen errores como "Unknown column" al agregar nuevos campos sin usar migraciones.
"""

import os
import sys
from app import create_app, db
from sqlalchemy import text

# Asegurarse de que la SECRET_KEY esté definida
os.environ['SECRET_KEY'] = 'clave-super-secreta-definida-en-fix-script'

def add_missing_columns():
    """
    Añade las columnas que faltan a la tabla de rutas para solucionar el error
    'Unknown column' cuando se han añadido nuevos campos al modelo Ruta.
    """
    app = create_app()
    with app.app_context():
        # Verificamos si las columnas ya existen
        try:
            with db.engine.connect() as connection:
                # Verificar si la columna 'activa' existe
                result = connection.execute(text("SHOW COLUMNS FROM rutas LIKE 'activa'"))
                activa_exists = result.fetchone() is not None
                
                # Verificar si la columna 'tiene_rampa' existe
                result = connection.execute(text("SHOW COLUMNS FROM rutas LIKE 'tiene_rampa'"))
                tiene_rampa_exists = result.fetchone() is not None
                
                # Verificar si la columna 'tiene_audio' existe
                result = connection.execute(text("SHOW COLUMNS FROM rutas LIKE 'tiene_audio'"))
                tiene_audio_exists = result.fetchone() is not None
                
                # Verificar si la columna 'tiene_espacio_silla' existe
                result = connection.execute(text("SHOW COLUMNS FROM rutas LIKE 'tiene_espacio_silla'"))
                tiene_espacio_silla_exists = result.fetchone() is not None
                
                # Verificar si la columna 'tiene_indicador_visual' existe
                result = connection.execute(text("SHOW COLUMNS FROM rutas LIKE 'tiene_indicador_visual'"))
                tiene_indicador_visual_exists = result.fetchone() is not None
                
                # Añadir las columnas que faltan
                if not activa_exists:
                    print("Añadiendo columna 'activa' a la tabla rutas...")
                    connection.execute(text("ALTER TABLE rutas ADD COLUMN activa TINYINT(1) DEFAULT 1;"))
                
                if not tiene_rampa_exists:
                    print("Añadiendo columna 'tiene_rampa' a la tabla rutas...")
                    connection.execute(text("ALTER TABLE rutas ADD COLUMN tiene_rampa TINYINT(1) DEFAULT 0;"))
                
                if not tiene_audio_exists:
                    print("Añadiendo columna 'tiene_audio' a la tabla rutas...")
                    connection.execute(text("ALTER TABLE rutas ADD COLUMN tiene_audio TINYINT(1) DEFAULT 0;"))
                
                if not tiene_espacio_silla_exists:
                    print("Añadiendo columna 'tiene_espacio_silla' a la tabla rutas...")
                    connection.execute(text("ALTER TABLE rutas ADD COLUMN tiene_espacio_silla TINYINT(1) DEFAULT 0;"))
                
                if not tiene_indicador_visual_exists:
                    print("Añadiendo columna 'tiene_indicador_visual' a la tabla rutas...")
                    connection.execute(text("ALTER TABLE rutas ADD COLUMN tiene_indicador_visual TINYINT(1) DEFAULT 0;"))
                
                # Confirmar los cambios
                connection.commit()
                
            print("¡Base de datos actualizada con éxito!")
        
        except Exception as e:
            print(f"Error al actualizar la base de datos: {e}")
            sys.exit(1)

if __name__ == "__main__":
    print("Actualizando la estructura de la base de datos...")
    add_missing_columns()
    print("Proceso completado.")
