# Actualización de la Base de Datos

Para solucionar el error de columnas desconocidas en la base de datos, ejecuta el siguiente script:

## Windows (PowerShell)

```powershell
cd backend
python fix_sqlalchemy.py
```

## Linux/Mac

```bash
cd backend
python fix_sqlalchemy.py
```

Este script añadirá las siguientes columnas a la tabla `rutas`:
- `activa` (TINYINT, default 1)
- `tiene_rampa` (TINYINT, default 0)
- `tiene_audio` (TINYINT, default 0)
- `tiene_espacio_silla` (TINYINT, default 0)
- `tiene_indicador_visual` (TINYINT, default 0)

Después de ejecutar el script, reinicia la aplicación:

```bash
python run.py
```

Si continúas experimentando problemas, revisa el documento de solución de problemas en `docs/solucion_problemas.md`.
