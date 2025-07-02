import os
# Establecer la variable de entorno SECRET_KEY directamente antes de importar la app
os.environ['SECRET_KEY'] = 'clave-super-secreta-definida-en-run-direct-py-2025'

import sys
from pathlib import Path

# Asegurarse de que la ruta al proyecto esté en sys.path
project_root = Path(__file__).parent.absolute()
sys.path.insert(0, str(project_root))

from app import create_app

app = create_app()

# Verificación explícita de la clave secreta
if not app.secret_key:
    print("ADVERTENCIA: La clave secreta no está configurada. Configurando una clave por defecto.")
    app.secret_key = os.urandom(24)
else:
    print(f"Clave secreta configurada correctamente. Longitud: {len(app.secret_key)} bytes")

# Verificar la ubicación de las plantillas
print(f"Directorio de plantillas: {app.template_folder}")
print(f"Directorios de búsqueda: {app.jinja_loader.searchpath}")

if __name__ == '__main__':
    app.run(debug=True)
