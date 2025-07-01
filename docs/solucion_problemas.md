# Solución de Problemas Comunes

## Problemas con Flask

### Error: "No module named 'flask'"
Este error indica que Flask no está instalado en tu entorno virtual. Solución:
```
pip install flask
```

### Error al ejecutar `flask run`
Si al ejecutar `flask run` no reconoce el comando, prueba:
```
python -m flask run
```

Si sigue sin funcionar, asegúrate de haber activado el entorno virtual:
```
venv\Scripts\activate  # Windows
source venv/bin/activate  # macOS/Linux
```

## Problemas con la base de datos

### Error de conexión a MySQL
Si obtienes errores de conexión a la base de datos:

1. Verifica que MySQL esté en ejecución en XAMPP
2. Verifica las credenciales en el archivo `.env`
3. Asegúrate de que la base de datos exista ejecutando:
   ```
   python setup_database.py
   ```

### Error: "No module named 'mysql.connector'"
Instala el conector de MySQL:
```
pip install mysql-connector-python
```

## Problemas con la aplicación

### Las plantillas no se cargan correctamente
Si tienes problemas con las plantillas de Flask:

1. Verifica que estás ejecutando Flask desde la carpeta correcta:
   ```
   cd backend
   set FLASK_APP=run.py
   flask run
   ```

2. Verifica la estructura de carpetas:
   - Las plantillas deben estar en `backend/app/templates/`
   - Los archivos estáticos deben estar en `backend/app/static/`

### Prueba simplificada

Si todos los pasos anteriores fallan, prueba una versión simplificada:
```
cd backend
python app_test.py
```

Esto ejecutará una versión básica de Flask. Si funciona, el problema está en la configuración de tu aplicación principal.

## Pasos para iniciar desde cero

Si deseas comenzar desde cero:

1. Activa el entorno virtual:
   ```
   venv\Scripts\activate  # Windows
   ```

2. Instala las dependencias básicas:
   ```
   pip install flask flask-sqlalchemy mysql-connector-python python-dotenv
   ```

3. Crea la base de datos:
   ```
   python setup_database.py
   ```

4. Ejecuta la aplicación de prueba:
   ```
   python app_test.py
   ```

5. Si funciona, intenta con la aplicación completa:
   ```
   set FLASK_APP=run.py
   flask run
   ```
