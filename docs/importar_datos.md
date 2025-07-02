# Guía de Importación de Datos

Este documento describe cómo utilizar la funcionalidad de importación de datos en el panel de administración del sistema de Transporte Accesible Cali. La importación permite cargar masivamente paradas, rutas y asociaciones entre rutas y paradas mediante archivos JSON.

## Acceso a la Funcionalidad

1. Inicie sesión con una cuenta de administrador
2. Navegue al Panel de Administración
3. Haga clic en "Importar Datos" en el menú lateral izquierdo

## Formatos de Archivo

Todos los archivos deben estar en formato JSON y contener un array (lista) de objetos. A continuación se describe la estructura para cada tipo de datos:

### 1. Paradas (Stops)

```json
[
  {
    "nombre": "Nombre de la Parada",
    "direccion": "Dirección de la parada",
    "latitud": 3.4516,
    "longitud": -76.5320,
    "tipo": "regular",
    "tiene_rampa": true,
    "tiene_semaforo_sonoro": false,
    "descripcion": "Descripción detallada de la parada"
  },
  {
    "nombre": "Otra Parada",
    "direccion": "Otra dirección",
    "latitud": 3.4550,
    "longitud": -76.5350,
    "tipo": "estacion",
    "tiene_rampa": true,
    "tiene_semaforo_sonoro": true,
    "descripcion": "Otra descripción"
  }
]
```

#### Campos para Paradas:

| Campo | Tipo | Requerido | Descripción |
|-------|------|-----------|-------------|
| nombre | String | Sí | Nombre identificativo de la parada |
| direccion | String | Sí | Dirección física de la parada |
| latitud | Float | Sí | Coordenada de latitud (entre -90 y 90) |
| longitud | Float | Sí | Coordenada de longitud (entre -180 y 180) |
| tipo | String | No | Tipo de parada: "regular", "estacion" o "terminal". Por defecto: "regular" |
| tiene_rampa | Boolean | No | Indica si la parada tiene rampa de acceso. Por defecto: false |
| tiene_semaforo_sonoro | Boolean | No | Indica si hay semáforo sonoro cerca. Por defecto: false |
| descripcion | String | No | Texto descriptivo sobre la parada |

### 2. Rutas (Routes)

```json
[
  {
    "numero": "R1",
    "nombre": "Ruta Centro - Norte",
    "origen": "Terminal Central",
    "destino": "Terminal Norte",
    "hora_inicio": "05:30",
    "hora_fin": "22:00",
    "frecuencia_minutos": 15,
    "descripcion": "Ruta que conecta el centro con la zona norte",
    "activa": true,
    "tiene_rampa": true,
    "tiene_audio": true,
    "tiene_espacio_silla": true,
    "tiene_indicador_visual": true,
    "coordenadas": [
      [3.4516, -76.5320],
      [3.4550, -76.5300],
      [3.4600, -76.5250],
      [3.4650, -76.5200]
    ]
  },
  {
    "numero": "R2",
    "nombre": "Ruta Centro - Sur",
    "origen": "Terminal Central",
    "destino": "Terminal Sur",
    "hora_inicio": "06:00",
    "hora_fin": "21:30",
    "frecuencia_minutos": 20,
    "descripcion": "Ruta que conecta el centro con la zona sur",
    "activa": true,
    "tiene_rampa": false,
    "tiene_audio": false,
    "tiene_espacio_silla": true,
    "tiene_indicador_visual": false,
    "coordenadas": [
      [3.4516, -76.5320],
      [3.4500, -76.5350],
      [3.4450, -76.5400]
    ]
  }
]
```

#### Campos para Rutas:

| Campo | Tipo | Requerido | Descripción |
|-------|------|-----------|-------------|
| numero | String | Sí | Código único de identificación de la ruta |
| nombre | String | Sí | Nombre descriptivo de la ruta |
| origen | String | Sí | Lugar de origen de la ruta |
| destino | String | Sí | Lugar de destino de la ruta |
| hora_inicio | String | Sí | Hora de inicio del servicio (formato "HH:MM") |
| hora_fin | String | Sí | Hora de finalización del servicio (formato "HH:MM") |
| frecuencia_minutos | Integer | No | Frecuencia de paso en minutos. Por defecto: 15 |
| descripcion | String | No | Texto descriptivo sobre la ruta |
| activa | Boolean | No | Indica si la ruta está actualmente operativa. Por defecto: true |
| tiene_rampa | Boolean | No | Indica si los vehículos tienen rampa de acceso. Por defecto: false |
| tiene_audio | Boolean | No | Indica si hay anuncios de audio. Por defecto: false |
| tiene_espacio_silla | Boolean | No | Indica si hay espacio para sillas de ruedas. Por defecto: false |
| tiene_indicador_visual | Boolean | No | Indica si hay indicadores visuales. Por defecto: false |
| coordenadas | Array | No | Lista de pares [latitud, longitud] que definen el trazado de la ruta en el mapa |

### 3. Asociaciones Ruta-Parada

```json
[
  {
    "ruta_numero": "R1",
    "parada_nombre": "Parada Centro",
    "orden": 1,
    "tiempo_estimado": 0
  },
  {
    "ruta_numero": "R1",
    "parada_nombre": "Otra Parada",
    "orden": 2,
    "tiempo_estimado": 8
  },
  {
    "ruta_numero": "R2",
    "parada_nombre": "Parada Centro",
    "orden": 1,
    "tiempo_estimado": 0
  }
]
```

#### Campos para Asociaciones Ruta-Parada:

| Campo | Tipo | Requerido | Descripción |
|-------|------|-----------|-------------|
| ruta_numero | String | Sí | Número de la ruta (debe existir previamente) |
| parada_nombre | String | Sí | Nombre de la parada (debe existir previamente) |
| orden | Integer | No | Orden secuencial de la parada en la ruta. Por defecto: 1 |
| tiempo_estimado | Integer | No | Tiempo estimado en minutos desde el origen. Por defecto: 0 |

## Instrucciones de Uso

1. **Seleccione el tipo de datos** que desea importar: paradas, rutas o asociaciones ruta-parada
2. **Elija un archivo JSON** con la estructura correcta
3. **Active "Vista previa"** para verificar los datos antes de importarlos (importante: la vista previa es necesaria antes de importar)
4. Revise los datos en la tabla de vista previa
5. Para rutas, también podrá ver una previsualización de los trazados en el mapa
6. Haga clic en **"Confirmar y Guardar Datos"** para guardar la información en la base de datos

## Consideraciones Importantes

- **IMPORTANTE**: Siempre use la opción "Vista previa" antes de importar cualquier dato. Esto es necesario para el correcto funcionamiento del sistema.
- Antes de importar asociaciones ruta-parada, asegúrese de que tanto las rutas como las paradas ya existan en el sistema.
- Los campos marcados como requeridos deben estar presentes en todos los objetos del archivo JSON.
- Para las rutas, las coordenadas deben seguir el formato exacto: array de arrays, donde cada subarray contiene [latitud, longitud].
- Las horas deben estar en formato "HH:MM" (24 horas).
- Los valores booleanos deben ser `true` o `false` (sin comillas).
- El sistema validará los datos antes de importarlos y mostrará mensajes de error si hay problemas.
- **Importante**: La vista previa de los datos es obligatoria antes de guardar. Si cierra la sesión o actualiza la página después de la vista previa, deberá subir el archivo nuevamente.
- **Registros duplicados**: Si intenta importar una ruta o parada con un identificador (número o nombre) que ya existe en el sistema, se actualizará el registro existente con los nuevos datos proporcionados en lugar de crear uno nuevo.

## Solución de Problemas Comunes

### Error: 'csrf_token' is undefined o Error de CSRF

Si recibe un error relacionado con el token CSRF al intentar importar datos:

1. Asegúrese de usar el botón de vista previa para verificar los datos antes de guardar
2. No modifique manualmente las URLs ni actualice la página durante el proceso de importación
3. No deje la página de vista previa abierta por mucho tiempo, ya que el token CSRF puede expirar
4. Evite utilizar la función de retroceso del navegador durante el proceso de importación
5. Si el problema persiste, cierre sesión, vuelva a iniciar sesión e intente nuevamente

### Error al guardar datos después de la vista previa

Si ve los datos correctamente en la vista previa pero ocurre un error al guardarlos:

1. Verifique que su sesión no haya expirado (inicie sesión nuevamente si es necesario)
2. Asegúrese de que no haya registros duplicados (especialmente para paradas o rutas con nombres/números que ya existen)
3. Compruebe que el formato de los datos sea correcto según las especificaciones anteriores

### Error de registros duplicados

Si recibe un error de registro duplicado como:
```
Error al guardar los datos: (pymysql.err.IntegrityError) (1062, "Duplicate entry 'XX' for key 'numero'")
```

Esto significa que está intentando importar un registro con un identificador (número de ruta o nombre de parada) que ya existe en el sistema. Considere lo siguiente:

1. El sistema ahora actualizará automáticamente los registros existentes en lugar de intentar crear duplicados
2. Si recibe este error, asegúrese de que tiene la última versión del sistema
3. Si el problema persiste, verifique que no haya entradas duplicadas en su archivo de importación
4. También puede editar manualmente el archivo JSON para cambiar los identificadores o eliminar las entradas duplicadas

Nota: Es recomendable revisar los datos existentes antes de realizar una importación masiva para evitar conflictos.

## Ejemplo Completo

A continuación se muestra un ejemplo de flujo de trabajo completo para configurar una nueva ruta:

1. Primero, importe las paradas:

```json
[
  {
    "nombre": "Terminal Central",
    "direccion": "Carrera 1 #25-45",
    "latitud": 3.4516,
    "longitud": -76.5320,
    "tipo": "terminal",
    "tiene_rampa": true,
    "tiene_semaforo_sonoro": true,
    "descripcion": "Terminal principal ubicada en el centro de la ciudad"
  },
  {
    "nombre": "Parada Hospital",
    "direccion": "Carrera 1 #30-15",
    "latitud": 3.4550,
    "longitud": -76.5300,
    "tipo": "regular",
    "tiene_rampa": true,
    "tiene_semaforo_sonoro": false,
    "descripcion": "Parada frente al Hospital Universitario"
  },
  {
    "nombre": "Terminal Norte",
    "direccion": "Avenida 2N #45-80",
    "latitud": 3.4650,
    "longitud": -76.5200,
    "tipo": "terminal",
    "tiene_rampa": true,
    "tiene_semaforo_sonoro": true,
    "descripcion": "Terminal ubicada en la zona norte"
  }
]
```

2. Luego, importe la ruta con su trazado:

```json
[
  {
    "numero": "R1",
    "nombre": "Ruta Centro - Norte",
    "origen": "Terminal Central",
    "destino": "Terminal Norte",
    "hora_inicio": "05:30",
    "hora_fin": "22:00",
    "frecuencia_minutos": 15,
    "descripcion": "Ruta principal que conecta el centro con la zona norte",
    "activa": true,
    "tiene_rampa": true,
    "tiene_audio": true,
    "tiene_espacio_silla": true,
    "tiene_indicador_visual": true,
    "coordenadas": [
      [3.4516, -76.5320],
      [3.4530, -76.5310],
      [3.4550, -76.5300],
      [3.4600, -76.5250],
      [3.4630, -76.5220],
      [3.4650, -76.5200]
    ]
  }
]
```

3. Finalmente, asocie las paradas a la ruta:

```json
[
  {
    "ruta_numero": "R1",
    "parada_nombre": "Terminal Central",
    "orden": 1,
    "tiempo_estimado": 0
  },
  {
    "ruta_numero": "R1",
    "parada_nombre": "Parada Hospital",
    "orden": 2,
    "tiempo_estimado": 5
  },
  {
    "ruta_numero": "R1",
    "parada_nombre": "Terminal Norte",
    "orden": 3,
    "tiempo_estimado": 15
  }
]
```

Con estos tres pasos, habrá configurado completamente una nueva ruta con sus paradas y trazado en el mapa.
