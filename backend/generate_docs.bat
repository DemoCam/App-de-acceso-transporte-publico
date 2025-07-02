@echo off
ECHO === Generando paquete de documentacion completo ===
ECHO.

REM Verificar que estamos en el directorio correcto
IF NOT EXIST run.py (
    ECHO Error: Este script debe ejecutarse desde la carpeta backend
    EXIT /B 1
)

ECHO Verificando dependencias...
pip list | findstr "Markdown" >NUL
IF ERRORLEVEL 1 (
    ECHO Instalando dependencias necesarias...
    pip install Markdown==3.5.2
)

ECHO Generando documentacion...
python generate_docs.py

ECHO.
ECHO === Proceso completo ===
ECHO.
ECHO El paquete de documentacion esta disponible en la carpeta "dist"
ECHO.
