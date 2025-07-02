#!/bin/bash

echo "=== Generando paquete de documentación completo ==="
echo ""

# Verificar que estamos en el directorio correcto
if [ ! -f "run.py" ]; then
    echo "Error: Este script debe ejecutarse desde la carpeta backend"
    exit 1
fi

echo "Verificando dependencias..."
if ! pip list | grep -q "Markdown"; then
    echo "Instalando dependencias necesarias..."
    pip install Markdown==3.5.2
fi

echo "Generando documentación..."
python generate_docs.py

echo ""
echo "=== Proceso completo ==="
echo ""
echo "El paquete de documentación está disponible en la carpeta \"dist\""
echo ""
