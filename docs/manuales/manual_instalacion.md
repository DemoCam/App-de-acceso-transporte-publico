# Guía de Instalación - App de Transporte Accesible Cali

## Índice
1. [Requisitos previos](#requisitos-previos)
2. [Instalación del entorno](#instalación-del-entorno)
3. [Configuración de la base de datos](#configuración-de-la-base-datos)
4. [Configuración de la aplicación](#configuración-de-la-aplicación)
5. [Ejecución de la aplicación](#ejecución-de-la-aplicación)
6. [Despliegue en producción](#despliegue-en-producción)
7. [Actualización de la base de datos](#actualización-de-la-base-datos)
8. [Problemas comunes](#problemas-comunes)

## Requisitos previos

Antes de comenzar la instalación, asegúrese de contar con los siguientes componentes:

### Software requerido:
- Python 3.8 o superior
- MySQL 8.0 o superior
- Git (para clonar el repositorio)
- Navegador web compatible (Chrome, Firefox, Edge o Safari)

### Requisitos de hardware recomendados:
- CPU: 2 núcleos o más
- RAM: 2GB mínimo, 4GB recomendado
- Almacenamiento: 1GB disponible mínimo
- Conexión a internet (para servicios externos y API)

## Instalación del entorno

### 1. Clonar el repositorio

```bash
# Windows
git clone https://github.com/DemoCam/App-de-acceso-transporte-publico.git
cd App-de-acceso-transporte-publico

# Linux/Mac
git clone https://github.com/DemoCam/App-de-acceso-transporte-publico.git
cd App-de-acceso-transporte-publico
```

### 2. Crear y activar entorno virtual

En Windows:
```bash
# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
venv\Scripts\activate
```

En Linux/Mac:
```bash
# Crear entorno virtual
python3 -m venv venv

# Activar entorno virtual
source venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

## Configuración de la base de datos

### 1. Preparar MySQL

Asegúrese de que MySQL esté instalado y en ejecución. Cree una base de datos para la aplicación:

```sql
CREATE DATABASE transporte_accesible_cali CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'app_transporte'@'localhost' IDENTIFIED BY 'password';
GRANT ALL PRIVILEGES ON transporte_accesible_cali.* TO 'app_transporte'@'localhost';
FLUSH PRIVILEGES;
```

**Nota**: Reemplace `'password'` por una contraseña segura.

### 2. Configurar variables de entorno

Cree un archivo `.env` en la raíz del proyecto con el siguiente contenido:

```
FLASK_APP=run.py
FLASK_ENV=development
SECRET_KEY=clave-super-secreta-para-produccion
DATABASE_URL=mysql+pymysql://app_transporte:password@localhost/transporte_accesible_cali
```

**Nota**: Reemplace `password` con la contraseña que estableció para el usuario MySQL.

### 3. Inicializar la base de datos

```bash
# Navegar al directorio backend
cd backend

# Inicializar la base de datos
python setup_database.py
```

## Configuración de la aplicación

### 1. Archivos de configuración

Si necesita modificar la configuración predeterminada, puede editar los siguientes archivos:

- `backend/app/__init__.py`: Configuración principal de Flask
- `backend/app/config.py`: Variables de configuración

### 2. Configurar servicios externos (opcional)

Si desea integrar con servicios externos como el API del MIO, edite el archivo de configuración para incluir las credenciales necesarias:

```bash
# Abrir archivo de configuración
# Windows:
notepad backend/app/services/mio_service.py

# Linux/Mac:
nano backend/app/services/mio_service.py
```

## Ejecución de la aplicación

### 1. Ejecutar la aplicación en modo desarrollo

```bash
# Navegar al directorio backend si no está allí
cd backend

# Ejecutar la aplicación
python run.py
```

La aplicación estará disponible en: [http://localhost:5000](http://localhost:5000)

### 2. Credenciales predeterminadas

Para el primer inicio de sesión, utilice:
- Usuario: `admin`
- Contraseña: `Reset2025!`

**IMPORTANTE**: Cambie estas credenciales inmediatamente después del primer inicio de sesión.

## Despliegue en producción

### 1. Configuración para producción

Para un entorno de producción, modifique el archivo `.env`:

```
FLASK_APP=run.py
FLASK_ENV=production
SECRET_KEY=generate_strong_random_key_here
DATABASE_URL=mysql+pymysql://usuario:contraseña@host/basededatos
```

### 2. Opciones de despliegue

#### Opción A: Servidor WSGI (Gunicorn)

Instale Gunicorn:
```bash
pip install gunicorn
```

Ejecute la aplicación:
```bash
gunicorn -w 4 -b 0.0.0.0:5000 "backend.run:app"
```

#### Opción B: Servidor web (Nginx + Gunicorn)

Instale Nginx y configure un proxy inverso a Gunicorn:

```nginx
server {
    listen 80;
    server_name yourdomain.com;

    location / {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## Actualización de la base de datos

Si necesita actualizar la estructura de la base de datos después de cambios en los modelos:

```bash
cd backend
python update_database.py
```

En caso de problemas con la actualización:

```bash
python fix_sqlalchemy.py
```

## Problemas comunes

### Error de conexión a la base de datos

Verificar:
- MySQL está en ejecución
- Las credenciales en el archivo `.env` son correctas
- El usuario tiene permisos sobre la base de datos

### Error "ModuleNotFoundError"

Solución:
- Asegurarse que el entorno virtual está activado
- Reinstalar dependencias: `pip install -r requirements.txt`

### Problemas con la migración de la base de datos

Si hay errores con tablas o columnas:

```bash
cd backend
python init_db.py  # ¡CUIDADO! Esto recrea toda la base de datos
```

### El asistente de voz no funciona

Verificar:
- El navegador es compatible (Chrome, Edge o Safari)
- Los permisos de micrófono están concedidos
- Hay conexión a internet para el reconocimiento de voz
