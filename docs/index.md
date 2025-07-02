# Documentación - App de Transporte Accesible Cali

Este directorio contiene toda la documentación del proyecto, incluyendo manuales de usuario, guías de instalación, y documentación técnica.

## Manuales

- [Manual de Usuario](manuales/manual_usuario.md) - Guía completa para usuarios finales
- [Manual de Instalación](manuales/manual_instalacion.md) - Instrucciones paso a paso para instalar la aplicación
- [Documentación de la API](manuales/api_reference.md) - Referencia técnica para desarrolladores

## Guías y tutoriales

- [Guía de accesibilidad](accesibilidad.md) - Información sobre características de accesibilidad
- [Asistente de voz](asistente_voz.md) - Guía para utilizar el asistente de voz
- [Herramientas de accesibilidad](herramientas_accesibilidad.md) - Descripción detallada de herramientas de accesibilidad

## Soporte técnico

- [Solución de problemas](solucion_problemas.md) - Soluciones a problemas comunes
- [Importación de datos](importar_datos.md) - Guía para importar datos externos

## Descargar paquete completo

Para generar un paquete descargable con toda la documentación:

```bash
cd backend
python generate_docs.py
```

El paquete estará disponible en la carpeta `dist/` y también en la aplicación web en la sección de ayuda.
