# 💰 Préstamos Gota a Gota / Daily Microloan App

> Aplicación de gestión de préstamos con pagos diarios, semanales, quincenales y mensuales.  
> Loan management app with daily, weekly, biweekly, and monthly payments.

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
git clone https://github.com/ChristhianC5Develop/prestamos-gota-a-gota.git
cd prestamos-gota-a-gota

# Crear entorno virtual / Create virtual environment
python -m venv venv
source venv/bin/activate  # en Windows: venv\Scripts\activate

# Instalar dependencias / Install dependencies
pip install -r backend/requirements.txt

# Ejecutar backend / Run backend
cd backend
uvicorn app.main:app --reload
