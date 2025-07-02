# 🚍 App de Transporte Accesible – Cali

Aplicación web enfocada en asistir a personas con discapacidad visual en la consulta y uso del transporte público en la ciudad de Cali. Proporciona información sobre rutas, paradas, y características de accesibilidad con una interfaz especialmente diseñada para ser compatible con lectores de pantalla y otras tecnologías asistivas.

## 👥 Equipo de desarrollo

- Jean Carlos Campo García – Scrum Master
- María Victoria Carabalí Caicedo – Product Owner
- Juan Camilo Valencia Burbano – Desarrollador

## 📦 Tecnologías utilizadas

- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **Backend**: Python + Flask
- **Base de Datos**: MySQL
- **Características de Accesibilidad**: Asistente de voz, alto contraste, redimensionado de texto
- **Herramientas**: GitHub, Trello, Postman

## 🌟 Características principales

- **Panel de administración** para gestión de rutas, paradas y usuarios
- **Autenticación y control de acceso** con diferentes roles de usuario
- **Consulta de rutas de transporte** con filtros por origen, destino y características
- **Visualización de paradas cercanas** con información detallada sobre accesibilidad
- **Asistente de voz incorporado** que puede ser silenciado según preferencia del usuario
- **Herramientas de accesibilidad** como alto contraste y ajuste de tamaño de texto
- **Interfaz adaptable** para diferentes dispositivos y tecnologías asistivas

## 📁 Estructura del proyecto

```
app-transporte-accesible-cali/
├── backend/                 # Lógica de negocio y API REST
│   ├── app/                 # Aplicación principal
│   │   ├── models/          # Modelos de datos
│   │   ├── routes/          # Controladores y endpoints
│   │   ├── templates/       # Plantillas HTML
│   │   ├── static/          # Archivos estáticos (CSS, JS, imágenes)
│   │   └── services/        # Servicios de integración
│   └── run.py               # Script para ejecutar la aplicación
├── docs/                    # Documentación técnica
└── README.md
```

## 🚀 Instalación y configuración

### Requisitos previos
- Python 3.8+
- MySQL 8.0+
- Git

### Pasos de instalación

1. Clonar el repositorio:
```bash
git clone https://github.com/DemoCam/App-de-acceso-transporte-publico.git
cd App-de-acceso-transporte-publico
```

2. Crear entorno virtual e instalar dependencias:
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. Configurar la base de datos:
```bash
cd backend
python setup_database.py
```

4. Ejecutar la aplicación:
```bash
python run.py
```

5. Acceder a la aplicación:
   - URL: [http://localhost:5000](http://localhost:5000)
   - Usuario administrador: admin
   - Contraseña: Reset2025!

## 🔁 Flujo de trabajo con Git

1. Clona el repositorio:
```bash
git clone https://github.com/DemoCam/App-de-acceso-transporte-publico.git
```

2. Crea una nueva rama para tu tarea:
```bash
git checkout -b feature/nombre-funcionalidad
```

3. Guarda tus cambios:
```bash
git add .
git commit -m "Descripción del cambio"
git push origin feature/nombre-funcionalidad
```

4. Ve a GitHub y crea un **Pull Request** hacia la rama `main`.

## 📌 Estado actual del proyecto

- [x] SRS completo  
- [x] Historias de usuario creadas e implementadas
- [x] Repositorio configurado y en desarrollo activo
- [x] Desarrollo del frontend con Bootstrap 5
- [x] Implementación de autenticación y control de acceso
- [x] Implementación del panel de administración
- [x] Funcionalidades de accesibilidad (asistente de voz, alto contraste)
- [x] Consulta de rutas y paradas con filtros
- [ ] Pruebas de usabilidad con usuarios
- [ ] Optimización para dispositivos móviles
- [ ] Documentación completa de la API

## 🛠️ Solución de problemas comunes

Si encuentra problemas al actualizar modelos de datos, ejecute:
```bash
python -c "from app import db; db.create_all()"
```

Si aparecen errores relacionados con columnas desconocidas en la base de datos, puede ser necesario ejecutar un script de migración manual:
```bash
cd backend
python fix_sqlalchemy.py
```

## 📄 Licencia

Este proyecto está bajo la licencia MIT. Ver el archivo LICENSE para más detalles.

## 🔗 Enlaces

- [Repositorio GitHub](https://github.com/DemoCam/App-de-acceso-transporte-publico.git)
- [Documentación](docs/)