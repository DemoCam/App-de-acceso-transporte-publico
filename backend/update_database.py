import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

def update_database():
    """
    Actualiza la estructura de la base de datos para añadir los nuevos campos a la tabla rutas
    """
    try:
        # Conectar a MySQL
        connection = mysql.connector.connect(
            host=os.environ.get('DATABASE_HOST', 'localhost'),
            user=os.environ.get('DATABASE_USER', 'root'),
            password=os.environ.get('DATABASE_PASSWORD', ''),
            database=os.environ.get('DATABASE_NAME', 'transporte_accesible_cali')
        )
        
        if connection.is_connected():
            cursor = connection.cursor()
            
            # Actualizar la tabla rutas para añadir los nuevos campos
            print("Actualizando la tabla rutas...")
            
            # Añadir columna 'activa'
            try:
                cursor.execute("ALTER TABLE rutas ADD COLUMN activa BOOLEAN DEFAULT TRUE")
                print("Columna 'activa' añadida correctamente")
            except Error as e:
                if "Duplicate column name" in str(e):
                    print("La columna 'activa' ya existe")
                else:
                    print(f"Error al añadir columna 'activa': {e}")
            
            # Añadir columna 'tiene_rampa'
            try:
                cursor.execute("ALTER TABLE rutas ADD COLUMN tiene_rampa BOOLEAN DEFAULT FALSE")
                print("Columna 'tiene_rampa' añadida correctamente")
            except Error as e:
                if "Duplicate column name" in str(e):
                    print("La columna 'tiene_rampa' ya existe")
                else:
                    print(f"Error al añadir columna 'tiene_rampa': {e}")
            
            # Añadir columna 'tiene_audio'
            try:
                cursor.execute("ALTER TABLE rutas ADD COLUMN tiene_audio BOOLEAN DEFAULT FALSE")
                print("Columna 'tiene_audio' añadida correctamente")
            except Error as e:
                if "Duplicate column name" in str(e):
                    print("La columna 'tiene_audio' ya existe")
                else:
                    print(f"Error al añadir columna 'tiene_audio': {e}")
                    
            # Añadir columna 'coordenadas' para el trazado de rutas en el mapa
            try:
                cursor.execute("ALTER TABLE rutas ADD COLUMN coordenadas TEXT NULL COMMENT 'Arreglo de coordenadas [lat, lng] para el trazado de la ruta'")
                print("Columna 'coordenadas' añadida correctamente")
            except Error as e:
                if "Duplicate column name" in str(e):
                    print("La columna 'coordenadas' ya existe")
                else:
                    print(f"Error al añadir columna 'coordenadas': {e}")
            
            # Añadir columna 'tiene_espacio_silla'
            try:
                cursor.execute("ALTER TABLE rutas ADD COLUMN tiene_espacio_silla BOOLEAN DEFAULT FALSE")
                print("Columna 'tiene_espacio_silla' añadida correctamente")
            except Error as e:
                if "Duplicate column name" in str(e):
                    print("La columna 'tiene_espacio_silla' ya existe")
                else:
                    print(f"Error al añadir columna 'tiene_espacio_silla': {e}")
            
            # Añadir columna 'tiene_indicador_visual'
            try:
                cursor.execute("ALTER TABLE rutas ADD COLUMN tiene_indicador_visual BOOLEAN DEFAULT FALSE")
                print("Columna 'tiene_indicador_visual' añadida correctamente")
            except Error as e:
                if "Duplicate column name" in str(e):
                    print("La columna 'tiene_indicador_visual' ya existe")
                else:
                    print(f"Error al añadir columna 'tiene_indicador_visual': {e}")
            
            connection.commit()
            print("Estructura de la base de datos actualizada correctamente")
            
    except Error as e:
        print(f"Error al conectar a MySQL: {e}")
        
    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()
            print("Conexión a MySQL cerrada")

if __name__ == "__main__":
    update_database()
