# Préstamos Gota a Gota API

Sistema de gestión de préstamos gota a gota con FastAPI.

## 🚀 Características

- Gestión completa de préstamos
- Seguimiento de pagos diarios/semanales/quincenales/mensuales
- Sistema de autenticación JWT
- API RESTful documentada
- Soporte multilenguaje (Español/Inglés)

## 🛠️ Tecnologías

- Python 3.10
- FastAPI
- SQLAlchemy
- MySQL
- JWT Authentication
- Pydantic
- Uvicorn

## 📋 Requisitos previos

- Python 3.10+
- MySQL Server
- pip (Python package installer)

## 🔧 Instalación

1. Clonar el repositorio:
```bash
git clone https://github.com/ChrithianC5Develop/prestamos-gota-a-gota.git
cd prestamos-gota-a-gota
```

2. Crear un entorno virtual:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. Instalar dependencias:
```bash
pip install -r requirements.txt
```

4. Configurar variables de entorno:
Crear archivo `.env` con:
```env
DB_HOST=localhost
DB_PORT=3306
DB_USER=tu_usuario
DB_PASSWORD=tu_contraseña
DB_NAME=prestamos_gota_a_gota
JWT_SECRET_KEY=tu_clave_secreta
API_V1_PREFIX=/api/v1
PROJECT_NAME=Prestamos Gota a Gota API
BACKEND_CORS_ORIGINS=["http://localhost:8000", "http://localhost:3000"]
```

5. Crear la base de datos:
```sql
CREATE DATABASE prestamos_gota_a_gota CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

6. Ejecutar la aplicación:
```bash
python run.py
```

## 📚 Documentación API

Una vez ejecutando, visita:
- Swagger UI: http://localhost:8000/api/v1/docs
- ReDoc: http://localhost:8000/api/v1/redoc

## 🔍 Endpoints principales

### Clientes
- POST /api/v1/clientes/ - Crear cliente
- GET /api/v1/clientes/ - Listar clientes
- GET /api/v1/clientes/{id} - Obtener cliente
- PUT /api/v1/clientes/{id} - Actualizar cliente
- DELETE /api/v1/clientes/{id} - Eliminar cliente

### Préstamos
- POST /api/v1/prestamos/ - Crear préstamo
- GET /api/v1/prestamos/ - Listar préstamos
- GET /api/v1/prestamos/{id} - Obtener préstamo
- PUT /api/v1/prestamos/{id} - Actualizar préstamo
- DELETE /api/v1/prestamos/{id} - Eliminar préstamo

### Pagos
- POST /api/v1/pagos/ - Registrar pago
- GET /api/v1/pagos/prestamo/{id} - Listar pagos de préstamo
- PUT /api/v1/pagos/{id} - Actualizar pago
- GET /api/v1/pagos/atrasados - Listar pagos atrasados

## 👥 Contribuir

1. Fork el proyecto
2. Crear una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abrir un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE.md](LICENSE.md) para detalles

---

## 🌍 Multilenguaje / Multi-language

Este sistema está diseñado para funcionar en **español e inglés**, permitiendo mayor alcance y adaptabilidad.  
This system is designed to support **Spanish and English**, allowing for greater reach and usability.

---

## 🚀 Tecnologías / Technologies

**Backend:**
- FastAPI (Python)
- SQLAlchemy / SQLite (MySQL listo para producción)
- JWT Auth
- OpenAPI (Swagger UI)
- Estructura limpia, modular y escalable

**Frontend Web:**
- Streamlit (Python)

**Frontend Móvil & Escritorio:**
- Kotlin Multiplatform (Compose)

---

## 📁 Módulos del Sistema / System Modules

- Gestión de usuarios con roles (admin, cobrador)
- Registro de clientes con validación única (cédula/RUC y correo)
- Creación de préstamos con configuraciones personalizadas
- Generación automática de cronograma de pagos
- Registro y control de cobros diarios
- Reportes diarios, mensuales y por cobrador

---

## 📸 Capturas / Screenshots

> *(Aquí se agregarán imágenes del sistema una vez desarrollado)*  
> *(Screenshots will be added once the system is developed)*

---

## ⚙️ Instalación / Installation

```bash
# Clonar el repositorio / Clone the repository
git clone https://github.com/ChrithianC5Develop/prestamos-gota-a-gota.git
cd prestamos-gota-a-gota

# Crear entorno virtual / Create virtual environment
python -m venv venv
source venv/bin/activate  # en Windows: venv\Scripts\activate

# Instalar dependencias / Install dependencies
pip install -r backend/requirements.txt

# Ejecutar backend / Run backend
cd backend
uvicorn app.main:app --reload
