"""
Script simplificado para crear un usuario administrador directamente en la base de datos
sin depender de la aplicación Flask ni requerir interacción
"""
import mysql.connector
import os
import sys
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash

# Cargar variables de entorno
load_dotenv()

def crear_admin_simple(password=None):
    """Crea un usuario superadmin con contraseña fija o la proporcionada"""
    try:
        # Si no se proporciona contraseña, usar una predeterminada
        if not password:
            password = "SuperAdmin2025!"
            
            # Si se pasó un argumento en la línea de comandos, usarlo como contraseña
            if len(sys.argv) > 1:
                password = sys.argv[1]
        
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
            
            # Verificar si ya existe un usuario administrador con username 'superadmin'
            cursor.execute("SELECT id FROM usuarios WHERE username = %s", ('superadmin',))
            admin_exists = cursor.fetchone()
            
            # Encriptar la contraseña
            password_hash = generate_password_hash(password)
            
            if admin_exists:
                # Actualizar la contraseña del usuario existente
                cursor.execute(
                    "UPDATE usuarios SET password_hash = %s WHERE username = %s",
                    (password_hash, 'superadmin')
                )
                connection.commit()
                print(f"La contraseña del usuario 'superadmin' ha sido actualizada correctamente a: {password}")
            else:
                # Crear un nuevo usuario administrador
                username = 'superadmin'
                email = 'superadmin@transporte-cali.com'
                nombre = 'Super'
                apellido = 'Admin'
                rol = 'admin'
                
                # Insertar el nuevo usuario
                cursor.execute(
                    """INSERT INTO usuarios (username, email, nombre, apellido, password_hash, rol, activo) 
                       VALUES (%s, %s, %s, %s, %s, %s, %s)""",
                    (username, email, nombre, apellido, password_hash, rol, True)
                )
                connection.commit()
                print(f"Usuario administrador '{username}' creado correctamente.")
                print(f"Email: {email}")
                print(f"Contraseña: {password}")
    
    except mysql.connector.Error as e:
        print(f"Error al conectar a MySQL: {e}")
        
    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()
            print("Conexión a MySQL cerrada")

if __name__ == "__main__":
    crear_admin_simple()
