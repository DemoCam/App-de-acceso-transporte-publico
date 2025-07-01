"""
Script de prueba para verificar la conexión a la base de datos MySQL
"""
import os
import sys
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

def test_mysql_connection():
    """Prueba la conexión a MySQL"""
    try:
        import mysql.connector
    except ImportError:
        print("Error: El módulo mysql-connector-python no está instalado.")
        print("Instálalo con: pip install mysql-connector-python")
        return False

    try:
        # Obtener variables de entorno
        db_user = os.environ.get('DATABASE_USER', 'root')
        db_password = os.environ.get('DATABASE_PASSWORD', '')
        db_host = os.environ.get('DATABASE_HOST', 'localhost')
        db_name = os.environ.get('DATABASE_NAME', 'transporte_accesible_cali')
        
        print(f"Intentando conectar a MySQL: {db_user}@{db_host}/{db_name}")
        
        # Intentar conectar sin la base de datos primero
        connection = mysql.connector.connect(
            host=db_host,
            user=db_user,
            password=db_password
        )
        
        if connection.is_connected():
            print("✅ Conexión a MySQL exitosa")
            cursor = connection.cursor()
            
            # Verificar si existe la base de datos
            cursor.execute(f"SHOW DATABASES LIKE '{db_name}'")
            result = cursor.fetchone()
            
            if result:
                print(f"✅ Base de datos '{db_name}' encontrada")
                
                # Intentar conectar a la base de datos específica
                connection.close()
                connection = mysql.connector.connect(
                    host=db_host,
                    user=db_user,
                    password=db_password,
                    database=db_name
                )
                
                if connection.is_connected():
                    print(f"✅ Conexión a la base de datos '{db_name}' exitosa")
                    
                    # Verificar tablas
                    cursor = connection.cursor()
                    cursor.execute("SHOW TABLES")
                    tables = cursor.fetchall()
                    
                    if tables:
                        print(f"✅ Tablas encontradas: {[table[0] for table in tables]}")
                    else:
                        print("⚠️ No se encontraron tablas en la base de datos")
                        return True
            else:
                print(f"❌ Base de datos '{db_name}' no encontrada")
                print(f"Creando base de datos '{db_name}'...")
                cursor.execute(f"CREATE DATABASE {db_name} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
                print(f"✅ Base de datos '{db_name}' creada correctamente")
            
            connection.close()
            return True
    
    except mysql.connector.Error as error:
        print(f"❌ Error al conectar a MySQL: {error}")
        return False
    
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return False

if __name__ == "__main__":
    print("Prueba de conexión a MySQL")
    print("-------------------------")
    
    if test_mysql_connection():
        print("\nPrueba completada exitosamente.")
        sys.exit(0)
    else:
        print("\nLa prueba falló. Revisa los mensajes de error.")
        sys.exit(1)
