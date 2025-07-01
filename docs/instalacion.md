# Guía de Instalación y Uso

Este documento proporciona las instrucciones para configurar y ejecutar la App de Transporte Accesible para personas con discapacidad visual en Cali.

## Requisitos previos

- Python 3.8 o superior
- MySQL 5.7 o superior
- Pip (gestor de paquetes de Python)

## Configuración inicial

1. Clona el repositorio:
```bash
git clone https://github.com/Yan24D/app-transporte-accesible-cali.git
cd app-transporte-accesible-cali
```

2. Crea un entorno virtual:
```bash
# En Windows
python -m venv venv
venv\Scripts\activate

# En macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

3. Instala las dependencias:
```bash
pip install -r requirements.txt
```

4. Configura las variables de entorno:
```bash
# En Windows
copy backend\.env.example backend\.env
# Edita el archivo .env con tus configuraciones

# En macOS/Linux
cp backend/.env.example backend/.env
# Edita el archivo .env con tus configuraciones
```

5. Crea la base de datos en MySQL:
```sql
CREATE DATABASE transporte_accesible_cali CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'usuario'@'localhost' IDENTIFIED BY 'contraseña';
GRANT ALL PRIVILEGES ON transporte_accesible_cali.* TO 'usuario'@'localhost';
FLUSH PRIVILEGES;
```

## Iniciar la aplicación

1. Navega a la carpeta de backend:
```bash
cd backend
```

2. Ejecuta la aplicación:
```bash
# En Windows
set FLASK_APP=run.py
set FLASK_ENV=development
flask run

# En macOS/Linux
export FLASK_APP=run.py
export FLASK_ENV=development
flask run
```

3. Abre tu navegador y ve a: `http://127.0.0.1:5000/`

## Migración de la base de datos (si es necesaria)

Si necesitas actualizar la estructura de la base de datos:

```bash
flask db init  # Solo la primera vez
flask db migrate -m "Descripción de los cambios"
flask db upgrade
```

## Cargar datos de ejemplo

Para cargar datos de ejemplo en la base de datos:

```bash
flask seed-db
```

## Pruebas

Para ejecutar las pruebas unitarias:

```bash
pytest
```

## Detener la aplicación

Presiona `Ctrl+C` en la terminal donde está ejecutándose Flask.
Para desactivar el entorno virtual:

```bash
deactivate
```

## Problemas comunes

### Error de conexión a MySQL

Asegúrate de que:
- El servicio de MySQL esté funcionando
- Las credenciales en el archivo .env sean correctas
- La base de datos exista

### Error al instalar mysqlclient

En Windows, puede que necesites instalar Microsoft Visual C++ Redistributable.
En Linux, puede que necesites instalar los paquetes de desarrollo de MySQL:

```bash
sudo apt-get install python3-dev default-libmysqlclient-dev build-essential
```
