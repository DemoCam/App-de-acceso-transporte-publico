import os
# Establecer la variable de entorno SECRET_KEY directamente antes de importar la app
os.environ['SECRET_KEY'] = 'clave-super-secreta-definida-en-run-py-2025'

from app import create_app

app = create_app()

# Verificación explícita de la clave secreta
if not app.secret_key:
    print("ADVERTENCIA: La clave secreta no está configurada. Configurando una clave por defecto.")
    app.secret_key = os.urandom(24)
else:
    print(f"Clave secreta configurada correctamente. Longitud: {len(app.secret_key)} bytes")

# Verificar que todos los modelos y tablas estén configurados correctamente
print("Verificando modelos y tablas de la aplicación...")

if __name__ == '__main__':
    app.run(debug=True)
