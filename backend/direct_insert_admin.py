"""
Script para insertar directamente un usuario administrador en la base de datos
usando la misma biblioteca werkzeug.security pero sin pasar por la aplicación Flask
"""
import os
import mysql.connector
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash

# Cargar variables de entorno
load_dotenv()

def insert_admin():
    """Inserta un usuario administrador directamente en la base de datos"""
    username = "admindb"
    password = "AdminDB2025!"
    email = "admindb@transporte-cali.com"
    nombre = "Admin DB"
    apellido = "Sistema"
    
    # Generar hash de la contraseña
    password_hash = generate_password_hash(password)
    
    print(f"Usuario a crear: {username}")
    print(f"Contraseña: {password}")
    print(f"Hash generado: {password_hash}")
    
    try:
        # Obtener credenciales de la base de datos
        db_user = os.environ.get('DATABASE_USER', 'root')
        db_password = os.environ.get('DATABASE_PASSWORD', '')
        db_host = os.environ.get('DATABASE_HOST', 'localhost')
        db_name = os.environ.get('DATABASE_NAME', 'transporte_accesible_cali')
        
        # Conectar a la base de datos
        connection = mysql.connector.connect(
            host=db_host,
            user=db_user,
            password=db_password,
            database=db_name
        )
        
        if connection.is_connected():
            cursor = connection.cursor()
            
            # Verificar si el usuario ya existe
            cursor.execute("SELECT id FROM usuarios WHERE username = %s", (username,))
            user_exists = cursor.fetchone()
            
            if user_exists:
                # Actualizar la contraseña
                cursor.execute(
                    "UPDATE usuarios SET password_hash = %s WHERE username = %s",
                    (password_hash, username)
                )
                connection.commit()
                print(f"Contraseña actualizada para el usuario '{username}'")
            else:
                # Insertar el nuevo usuario
                cursor.execute(
                    """INSERT INTO usuarios (username, email, nombre, apellido, password_hash, rol, activo) 
                       VALUES (%s, %s, %s, %s, %s, %s, %s)""",
                    (username, email, nombre, apellido, password_hash, 'admin', True)
                )
                connection.commit()
                print(f"Usuario '{username}' creado correctamente")
            
    except mysql.connector.Error as e:
        print(f"Error al conectar a MySQL: {e}")
        
    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()
            print("Conexión a MySQL cerrada")

if __name__ == "__main__":
    insert_admin()
