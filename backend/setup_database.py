import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

def create_database():
    """
    Crea la base de datos y las tablas necesarias para la aplicación
    """
    try:
        # Conectar a MySQL sin especificar base de datos
        connection = mysql.connector.connect(
            host=os.environ.get('DATABASE_HOST', 'localhost'),
            user=os.environ.get('DATABASE_USER', 'root'),
            password=os.environ.get('DATABASE_PASSWORD', '')
        )
        
        if connection.is_connected():
            cursor = connection.cursor()
            
            # Crear la base de datos si no existe
            db_name = os.environ.get('DATABASE_NAME', 'transporte_accesible_cali')
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
            print(f"Base de datos '{db_name}' creada o ya existente")
            
            # Usar la base de datos
            cursor.execute(f"USE {db_name}")
            
            # Crear tablas si no existen
            create_tables(cursor)
            
            connection.commit()
            print("Tablas creadas correctamente")
            
    except Error as e:
        print(f"Error al conectar a MySQL: {e}")
        
    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()
            print("Conexión a MySQL cerrada")

def create_tables(cursor):
    """
    Crea las tablas necesarias para la aplicación
    """
    # Tabla de usuarios
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuarios (
        id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(64) UNIQUE NOT NULL,
        email VARCHAR(120) UNIQUE NOT NULL,
        nombre VARCHAR(64) NOT NULL,
        apellido VARCHAR(64) NOT NULL,
        password_hash VARCHAR(128) NOT NULL,
        rol VARCHAR(20) DEFAULT 'usuario',
        activo BOOLEAN DEFAULT TRUE,
        fecha_registro DATETIME DEFAULT CURRENT_TIMESTAMP,
        fecha_ultimo_acceso DATETIME
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
    """)
    
    # Tabla de rutas
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS rutas (
        id INT AUTO_INCREMENT PRIMARY KEY,
        numero VARCHAR(10) UNIQUE NOT NULL,
        nombre VARCHAR(100) NOT NULL,
        origen VARCHAR(100) NOT NULL,
        destino VARCHAR(100) NOT NULL,
        hora_inicio TIME NOT NULL,
        hora_fin TIME NOT NULL,
        frecuencia_minutos INT DEFAULT 15,
        descripcion TEXT,
        activa BOOLEAN DEFAULT TRUE,
        tiene_rampa BOOLEAN DEFAULT FALSE,
        tiene_audio BOOLEAN DEFAULT FALSE,
        tiene_espacio_silla BOOLEAN DEFAULT FALSE,
        tiene_indicador_visual BOOLEAN DEFAULT FALSE
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
    """)
    
    # Tabla de paradas
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS paradas (
        id INT AUTO_INCREMENT PRIMARY KEY,
        nombre VARCHAR(100) NOT NULL,
        direccion VARCHAR(200) NOT NULL,
        latitud FLOAT NOT NULL,
        longitud FLOAT NOT NULL,
        tipo VARCHAR(50) DEFAULT 'regular',
        tiene_rampa BOOLEAN DEFAULT FALSE,
        tiene_semaforo_sonoro BOOLEAN DEFAULT FALSE,
        descripcion TEXT
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
    """)
    
    # Tabla de relación entre rutas y paradas
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS ruta_parada (
        ruta_id INT,
        parada_id INT,
        orden INT NOT NULL,
        tiempo_estimado INT,
        PRIMARY KEY (ruta_id, parada_id),
        FOREIGN KEY (ruta_id) REFERENCES rutas(id),
        FOREIGN KEY (parada_id) REFERENCES paradas(id)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
    """)
    
if __name__ == "__main__":
    create_database()
