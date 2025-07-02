# Solución de Problemas Comunes

Este documento proporciona soluciones a problemas comunes que podrían surgir durante el desarrollo o uso de la aplicación.

## Problemas con la Base de Datos

### Error: "Unknown column" en consultas SQL

Este error ocurre cuando se han añadido nuevos campos a los modelos de Python pero no se han actualizado las tablas correspondientes en la base de datos.

**Solución:**

1. Ejecutar el script de reparación de la base de datos:

```bash
cd backend
python fix_sqlalchemy.py
```

Este script verificará la estructura de la base de datos y añadirá las columnas que faltan.

### Error al ejecutar migraciones

Si estás teniendo problemas con las migraciones de base de datos:

```bash
cd backend
# Reiniciar las migraciones (solo si es necesario)
rm -rf migrations/
python -c "from app import db, create_app; app=create_app(); app.app_context().push(); db.create_all()"
```

## Problemas con la Autenticación

### No puedo iniciar sesión como administrador

Si has olvidado la contraseña del administrador o necesitas crear un nuevo usuario administrador:

```bash
cd backend
python -c "from app import db, create_app; from app.models.usuario import Usuario, Role; app=create_app(); app.app_context().push(); admin=Usuario(username='admin', email='admin@example.com', nombre='Admin', apellido='Sistema', rol=Role.ADMIN); admin.set_password('admin123'); db.session.add(admin); db.session.commit(); print('Administrador creado/actualizado correctamente')"
```

## Problemas con el Servidor

### El servidor no inicia

Verifica que todas las dependencias están instaladas:

```bash
pip install -r requirements.txt
```

Verifica que las variables de entorno están configuradas correctamente:

```bash
cd backend
python -c "import os; print('DATABASE_URI:', os.environ.get('DATABASE_URI', 'No configurado'))"
```

### Servidor se detiene con error

Si el servidor se detiene con un error, revisa los logs:

```bash
cd backend
cat error.log
```

## Problemas con los archivos estáticos

Si los archivos CSS o JavaScript no se cargan correctamente:

1. Verifica que los archivos existen en la carpeta `static`:

```bash
ls -la backend/app/static/css/
ls -la backend/app/static/js/
```

2. Limpia la caché del navegador y recarga la página.

## Problemas con las características de accesibilidad

### El asistente de voz no funciona

1. Verifica que el navegador tiene habilitado JavaScript.
2. Verifica que el navegador soporta la API de síntesis de voz (Web Speech API).
3. Verifica que los archivos JavaScript relacionados están cargados correctamente:

```bash
ls -la backend/app/static/js/asistente-voz.js
ls -la backend/app/static/js/asistente-voz-fixed.js
```

### Los botones de accesibilidad no funcionan

Verifica que el archivo `accesibilidad.js` está cargado correctamente:

```bash
ls -la backend/app/static/js/accesibilidad.js
```

## Contacto para soporte

Si no encuentras solución a tu problema, contacta al equipo de desarrollo:

- Email: soporte@transporte-accesible-cali.com
- GitHub: Abre un issue en https://github.com/DemoCam/App-de-acceso-transporte-publico/issues
