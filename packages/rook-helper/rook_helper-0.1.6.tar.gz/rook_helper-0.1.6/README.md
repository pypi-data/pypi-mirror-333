# 📌 Proyecto: README

## 📖 Tabla de Contenidos
1. [Instrucciones para probar](#instrucciones-para-probar)
2. [Pruebas y análisis](#pruebas-y-análisis)
3. [Compilación y distribución](#compilación-y-distribución)
4. [Uso del paquete](#uso-del-paquete)
5. [Paquetes habilitados](#paquetes-habilitados)

---

## 🚀 Instrucciones para probar

### 🔹 Clonar el repositorio
```bash
# Clona el repositorio desde GitHub
git clone <URL_DEL_REPOSITORIO>
cd <NOMBRE_DEL_PROYECTO>
```

### 🔹 Instalar dependencias
```bash
pip install -r requirements-dev.txt
```

---

## 🛠 Pruebas y análisis

### 🧪 Ejecutar pruebas
```bash
# Ejecuta todos los tests
python -m unittest discover

# Ejecuta un test específico
python -m unittest directory/test.py -k test_function
```

### ✅ Ejecutar el linter
```bash
tox -e lint
```

### 📊 Ejecutar test coverage
```bash
tox -e coverage
```

### 🔄 Ejecutar todas las pruebas y análisis
```bash
tox
```

### 🔍 Análisis de vulnerabilidades
```bash
tox -e security
```

---

## 📦 Compilación y distribución

### 🔹 Compilar el paquete
```bash
python setup.py sdist bdist_wheel
twine upload dist/*
```

### 🔹 Probar el paquete localmente
```bash
pip install -e .
```

---

## 📌 Uso del paquete

### 📂 Ruta para crear un JSON de un documento de un pilar
```python
from rook_helper.structure.body_health.blood_glucose_event import build_json
```

#### Ejemplo:
```python
from rook_helper.structure.pillar.data_structure import build_json
```

### 🛠 Ruta de un helper
```python
from rook_helper import package general
```

#### Ejemplo:
```python
from rook_helper import convert_to_type
```

---

## 📚 Paquetes habilitados

### 🔹 Helpers generales
- `remove_client_uuid_from_user_id`
- `format_datetime`
- `convert_to_type`

### 🔹 Helpers de estructura

#### 🏥 Body Health
- `blood_glucose_event`
- `blood_pressure_event`
- `body_metrics_event`
- `heart_rate_event`
- `hydration_event`
- `menstruation_event`
- `mood_event`
- `nutrition_event`
- `oxygenation_event`
- `temperature_event`
- `summary`

#### 🏃 Physical Health
- `calories_event`
- `heart_rate_event`
- `oxygenation_event`
- `steps_event`
- `stress_event`
- `activity_event`
- `summary`

#### 🌙 Sleep Health
- `summary`

#### 👤 User Information
- `information`

