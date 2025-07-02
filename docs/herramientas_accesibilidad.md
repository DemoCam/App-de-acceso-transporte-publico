# Herramientas de Accesibilidad

Este documento describe las herramientas de accesibilidad disponibles en la aplicación de Transporte Accesible Cali, incluyendo el Asistente de Voz y el Panel de Accesibilidad.

## Índice
1. [Panel Flotante de Accesibilidad](#panel-flotante-de-accesibilidad)
2. [Asistente de Voz](#asistente-de-voz)
3. [Atajos de Teclado](#atajos-de-teclado)
4. [Solución de Problemas Comunes](#solución-de-problemas-comunes)

## Panel Flotante de Accesibilidad

El Panel Flotante de Accesibilidad proporciona acceso rápido a varias opciones de accesibilidad. Se encuentra en la esquina inferior derecha de la pantalla, ubicado encima del botón del Asistente de Voz.

### Cómo acceder al panel
- Haz clic en el botón gris redondo con el ícono de accesibilidad universal.
- El panel se desplegará mostrando las siguientes opciones:

### Opciones disponibles

1. **Alto contraste**: Alterna el modo de alto contraste para mejorar la visibilidad para usuarios con baja visión.
2. **Aumentar texto**: Incrementa el tamaño de la fuente en toda la aplicación para facilitar la lectura.
3. **Silenciar/Activar voz**: Silencia o activa la salida de voz del asistente. Al silenciarlo, el asistente seguirá mostrando mensajes visuales pero no hablará.

### Posicionamiento

El panel flotante se encuentra posicionado encima del botón del Asistente de Voz para evitar superposiciones y garantizar que ambas herramientas estén accesibles en todo momento.

## Asistente de Voz

El Asistente de Voz permite interactuar con la aplicación mediante comandos de voz. Se encuentra en la esquina inferior derecha de la pantalla como un botón azul redondo con el ícono de un micrófono.

### Cómo activarlo
- Haz clic en el botón azul redondo con el ícono de micrófono.
- Utiliza el atajo de teclado `Alt + A`.
- Haz clic en el banner "Describir esta página" que aparece temporalmente al cargar cada página.

### Modos de funcionamiento

1. **Modo activo**: Cuando el botón es de color rojo, el asistente está escuchando activamente tus comandos.
2. **Modo inactivo**: Cuando el botón es de color azul, el asistente está disponible pero no está escuchando.
3. **Modo silenciado**: Cuando has silenciado el asistente desde el panel de accesibilidad, el asistente mostrará mensajes visuales pero no producirá salida de voz.

### Documentación completa

Para una guía detallada de todos los comandos disponibles, ejemplos de uso y solución de problemas, visita la sección "Asistente de Voz" en el menú principal de la aplicación o ve directamente a la URL `/asistente-voz`.

## Atajos de Teclado

Los siguientes atajos de teclado están disponibles para mejorar la accesibilidad:

| Atajo | Función |
|-------|---------|
| `Alt + A` | Activar/desactivar el asistente de voz |
| `Alt + H` | Mostrar ayuda sobre los comandos disponibles |
| `Alt + D` | Describir la página actual |
| `Tab` | Navegar entre elementos interactivos |
| `Esc` | Cerrar paneles o diálogos abiertos |

## Solución de Problemas Comunes

### Panel de Accesibilidad

1. **El panel no se abre al hacer clic en el botón**
   - Intenta actualizar la página
   - Verifica que no haya errores JavaScript en la consola del navegador

2. **Los cambios de configuración no persisten**
   - Verifica que tu navegador tenga habilitado el almacenamiento local (localStorage)
   - Asegúrate de que no estés en modo de navegación privada

### Asistente de Voz

1. **El botón de silencio no funciona**
   - Verifica que estés utilizando un navegador compatible (Chrome, Edge, Safari)
   - Intenta actualizar la página para reiniciar el asistente

2. **El asistente no responde a los comandos**
   - Asegúrate de tener habilitados los permisos de micrófono en tu navegador
   - Habla claramente y en un ambiente con poco ruido de fondo
   - Verifica que el asistente esté en modo activo (botón rojo)

3. **El asistente está activo pero no escucha**
   - Desactiva y vuelve a activar el asistente presionando `Alt + A` dos veces
   - Verifica que tu micrófono esté funcionando en otras aplicaciones
