# Documentación de la API - App de Transporte Accesible Cali

## Índice
1. [Introducción](#introducción)
2. [Autenticación](#autenticación)
3. [Formatos de respuesta](#formatos-de-respuesta)
4. [Endpoints de rutas](#endpoints-de-rutas)
5. [Endpoints de paradas](#endpoints-de-paradas)
6. [Endpoints de asociaciones](#endpoints-de-asociaciones)
7. [Integración con MIO](#integración-con-mio)
8. [Códigos de estado](#códigos-de-estado)
9. [Límites y paginación](#límites-y-paginación)
10. [Ejemplos de uso](#ejemplos-de-uso)

## Introducción

La API REST de la App de Transporte Accesible Cali proporciona acceso programático a la información de rutas, paradas y características de accesibilidad del sistema de transporte público de la ciudad.

### URL Base

```
http://[host]:[puerto]/api
```

En entorno de desarrollo local:
```
http://localhost:5000/api
```

## Autenticación

Actualmente, la API es de acceso público para endpoints de consulta. Para endpoints que modifiquen datos (si se implementan en el futuro), se requerirá autenticación mediante JWT.

## Formatos de respuesta

Todas las respuestas son devueltas en formato JSON con la siguiente estructura básica:

```json
{
  "status": "success",
  "data": [...]
}
```

En caso de error:

```json
{
  "status": "error",
  "message": "Descripción del error"
}
```

## Endpoints de rutas

### Obtener todas las rutas

**Endpoint:** `GET /api/rutas`

**Descripción:** Devuelve un listado de todas las rutas disponibles.

**Parámetros de consulta opcionales:**
- `accesible` (boolean): Filtrar por rutas con características de accesibilidad.

**Ejemplo de respuesta:**
```json
{
  "status": "success",
  "data": [
    {
      "id": 1,
      "numero": "A10",
      "nombre": "Terminal - Centro",
      "descripcion": "Ruta que va desde la terminal hasta el centro de la ciudad",
      "hora_inicio": "04:30",
      "hora_fin": "22:00",
      "intervalo_minutos": 12,
      "accesible": true,
      "tiene_rampa": true,
      "tiene_anuncios_audio": true
    },
    // Más rutas...
  ]
}
```

### Obtener una ruta específica

**Endpoint:** `GET /api/rutas/{ruta_id}`

**Descripción:** Devuelve la información detallada de una ruta específica, incluyendo sus paradas.

**Ejemplo de respuesta:**
```json
{
  "status": "success",
  "data": {
    "id": 1,
    "numero": "A10",
    "nombre": "Terminal - Centro",
    "descripcion": "Ruta que va desde la terminal hasta el centro de la ciudad",
    "hora_inicio": "04:30",
    "hora_fin": "22:00",
    "intervalo_minutos": 12,
    "accesible": true,
    "tiene_rampa": true,
    "tiene_anuncios_audio": true,
    "paradas": [
      {
        "id": 5,
        "nombre": "Terminal de Transportes",
        "direccion": "Calle 30N #2A-29",
        "orden": 1,
        "tiempo_estimado": 0
      },
      // Más paradas...
    ]
  }
}
```

## Endpoints de paradas

### Obtener todas las paradas

**Endpoint:** `GET /api/paradas`

**Descripción:** Devuelve un listado de todas las paradas disponibles.

**Parámetros de consulta opcionales:**
- `accesible` (boolean): Filtrar por paradas con características de accesibilidad.

**Ejemplo de respuesta:**
```json
{
  "status": "success",
  "data": [
    {
      "id": 1,
      "nombre": "Terminal de Transportes",
      "direccion": "Calle 30N #2A-29",
      "referencia": "Frente a la estación de servicio",
      "tiene_rampa": true,
      "tiene_semaforo_sonoro": false,
      "tiene_informacion_braille": true,
      "latitud": 3.458762,
      "longitud": -76.523354
    },
    // Más paradas...
  ]
}
```

### Obtener una parada específica

**Endpoint:** `GET /api/paradas/{parada_id}`

**Descripción:** Devuelve la información detallada de una parada específica.

**Ejemplo de respuesta:**
```json
{
  "status": "success",
  "data": {
    "id": 1,
    "nombre": "Terminal de Transportes",
    "direccion": "Calle 30N #2A-29",
    "referencia": "Frente a la estación de servicio",
    "tiene_rampa": true,
    "tiene_semaforo_sonoro": false,
    "tiene_informacion_braille": true,
    "latitud": 3.458762,
    "longitud": -76.523354
  }
}
```

### Obtener rutas por parada

**Endpoint:** `GET /api/paradas/{parada_id}/rutas`

**Descripción:** Devuelve todas las rutas que pasan por una parada específica.

**Ejemplo de respuesta:**
```json
{
  "status": "success",
  "data": [
    {
      "id": 1,
      "numero": "A10",
      "nombre": "Terminal - Centro",
      "descripcion": "Ruta que va desde la terminal hasta el centro de la ciudad",
      "hora_inicio": "04:30",
      "hora_fin": "22:00",
      "intervalo_minutos": 12,
      "accesible": true
    },
    // Más rutas...
  ]
}
```

## Endpoints de asociaciones

### Obtener asociaciones ruta-parada

**Endpoint:** `GET /api/rutas-paradas`

**Descripción:** Devuelve las asociaciones entre rutas y paradas.

**Parámetros de consulta:**
- `ruta_id` (integer, opcional): Filtrar por ID de ruta
- `parada_id` (integer, opcional): Filtrar por ID de parada

**Ejemplo de respuesta:**
```json
{
  "status": "success",
  "data": [
    {
      "ruta_id": 1,
      "ruta": {
        "numero": "A10",
        "nombre": "Terminal - Centro"
      },
      "parada_id": 5,
      "parada": {
        "nombre": "Terminal de Transportes",
        "direccion": "Calle 30N #2A-29"
      },
      "orden": 1,
      "tiempo_estimado": 0
    },
    // Más asociaciones...
  ]
}
```

## Integración con MIO

### Obtener rutas del MIO

**Endpoint:** `GET /api/mio/rutas`

**Descripción:** Obtiene información de rutas desde el servicio externo del MIO.

**Ejemplo de respuesta:**
```json
{
  "status": "success",
  "data": [
    {
      "codigo": "P10A",
      "nombre": "Universidades - Centro",
      "tipo": "Pretroncal",
      "inicio_operacion": "04:30",
      "fin_operacion": "23:00"
    },
    // Más rutas...
  ]
}
```

### Obtener paradas del MIO

**Endpoint:** `GET /api/mio/paradas`

**Descripción:** Obtiene información de paradas desde el servicio externo del MIO.

**Ejemplo de respuesta:**
```json
{
  "status": "success",
  "data": [
    {
      "codigo": "E31",
      "nombre": "Estación Universidades",
      "direccion": "Calle 13 con Carrera 100",
      "tipo": "Estación",
      "accesible": true
    },
    // Más paradas...
  ]
}
```

## Códigos de estado

La API utiliza los siguientes códigos de estado HTTP:

- `200 OK`: La solicitud se procesó correctamente
- `400 Bad Request`: La solicitud contiene parámetros incorrectos o faltantes
- `404 Not Found`: El recurso solicitado no existe
- `500 Internal Server Error`: Error interno del servidor

## Límites y paginación

Actualmente, la API no implementa límites de tasa ni paginación, pero podría hacerlo en el futuro para conjuntos de datos grandes.

### Paginación futura (cuando se implemente)

Parámetros previstos:
- `page`: Número de página (comenzando desde 1)
- `per_page`: Elementos por página (por defecto 20, máximo 100)

## Ejemplos de uso

### Python con Requests

```python
import requests

# Obtener todas las rutas
response = requests.get('http://localhost:5000/api/rutas')
rutas = response.json()['data']

# Obtener una parada específica
response = requests.get('http://localhost:5000/api/paradas/1')
parada = response.json()['data']

# Filtrar rutas por parada
response = requests.get('http://localhost:5000/api/paradas/1/rutas')
rutas_por_parada = response.json()['data']
```

### JavaScript con Fetch API

```javascript
// Obtener todas las paradas
fetch('http://localhost:5000/api/paradas')
  .then(response => response.json())
  .then(data => {
    const paradas = data.data;
    console.log(paradas);
  })
  .catch(error => console.error('Error:', error));

// Obtener rutas del MIO
fetch('http://localhost:5000/api/mio/rutas')
  .then(response => response.json())
  .then(data => {
    const rutasMio = data.data;
    console.log(rutasMio);
  })
  .catch(error => console.error('Error:', error));
```
