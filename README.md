# Préstamos Gota a Gota

Sistema profesional de gestión de préstamos con funcionalidades de cobranza y notificaciones.

## 🌟 Características

- Gestión de préstamos y pagos
- Sistema de cobranza con rutas
- Notificaciones multicanal
- Autenticación y autorización
- Reportes y estadísticas
- Interfaz multilingüe (Español/Inglés)

## 🛠️ Tecnologías

- Backend: FastAPI (Python)
- Base de datos: MySQL
- Autenticación: JWT
- Frontend Web: Streamlit
- Frontend Móvil/Desktop: Kotlin Multiplatform

## 📦 Instalación

1. Clonar el repositorio:
```bash
git clone https://github.com/tu-usuario/prestamos-gota-a-gota.git
cd prestamos-gota-a-gota
```

2. Crear y activar entorno virtual:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. Instalar dependencias:
```bash
pip install -e ".[dev]"
```

4. Configurar variables de entorno:
```bash
cp .env.example .env
# Editar .env con tus configuraciones
```

5. Iniciar la base de datos:
```bash
alembic upgrade head
```

6. Ejecutar el servidor:
```bash
uvicorn app.main:app --reload
```

## 📚 Documentación

La documentación de la API está disponible en:
- Swagger UI: `/api/v1/docs`
- ReDoc: `/api/v1/redoc`

## 🧪 Tests

Ejecutar los tests:
```bash
pytest
```

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para más detalles.

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
