# Tests del Sistema de Préstamos Gota a Gota

Este directorio contiene los tests unitarios y de integración para el sistema de préstamos.

## Estructura

```
tests/
├── __init__.py      # Inicialización del paquete
├── conftest.py      # Configuración y fixtures para pytest
├── test_*.py        # Tests individuales para cada componente
```

## Ejecutar los Tests

### Tests básicos

Para ejecutar todos los tests:

```bash
python -m pytest
```

Para ejecutar tests con información detallada:

```bash
python -m pytest -v
```

### Tests específicos

Para ejecutar un archivo de test específico:

```bash
python -m pytest tests/test_notificaciones.py
```

Para ejecutar un test específico:

```bash
python -m pytest tests/test_notificaciones.py::test_crear_notificacion
```

### Cobertura de tests

Para ejecutar los tests y obtener un reporte de cobertura:

```bash
python -m pytest --cov=app
```

Para un reporte de cobertura más detallado:

```bash
python -m pytest --cov=app --cov-report=html
```

Esto generará un reporte HTML en el directorio `htmlcov/` que puede ser abierto en un navegador web.

## Fixtures

Los principales fixtures definidos en `conftest.py` son:

- `db`: Proporciona una sesión de base de datos en memoria para tests
- `client`: Cliente de test para la API de FastAPI
- `test_user`: Usuario de prueba 
- `token`: Token JWT para autenticación
- `authorized_client`: Cliente autorizado con el token JWT
- `authenticated_user`: Usuario autenticado para dependencias de FastAPI

## Añadir Nuevos Tests

Al añadir nuevos tests, seguir las convenciones:

1. Nombre del archivo: `test_<componente>.py`
2. Nombre de las funciones de test: `test_<funcionalidad>`
3. Usar fixtures existentes cuando sea posible
4. Incluir documentación bilingüe (español/inglés)

## Buenas prácticas

- Mantener los tests independientes entre sí
- Usar nombres descriptivos para las funciones de test
- Proporcionar información clara en los mensajes de assert
- Limpiar después de cada test usando fixtures con yield
- Evitar estado compartido entre tests 