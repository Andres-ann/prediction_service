# 🧠 Microservicio de Predicción de Reservas

Este proyecto forma parte del **Trabajo Práctico de la materia: Programación de Vanguardia 2025**.  
Su objetivo es desarrollar un **microservicio escalable** en **Python (FastAPI)** que formará parte de una plataforma de gestión de reservas, incorporando en el futuro un módulo de **predicción de demanda**.

---

# 🎯 Objetivo del microservicio

Proveer endpoints que permitan consultar predicciones sobre la demanda de reservas (de salas, artículos, etc.) a partir del historial existente.

El microservicio se comunicará con la base de datos o con otro servicio que le provea los datos históricos, procesará la información y devolverá resultados como:

- **Nivel de ocupación esperado.**
- **Recursos con mayor probabilidad de ser reservados.**
- **Recomendaciones de asignación.**

---

## 🚀 Tecnologías utilizadas

- **Python 3.12+**
- **FastAPI**
- **Uvicorn**
- **Pydantic Settings**
- **SQLAlchemy**
- **psycopg2-binary**
- **python-dotenv**

---

## 📁 Estructura del proyecto

```
prediction_service/
├── app/
│   ├── main.py
│   ├── api/
│   │   └── routes_health.py
│   ├── core/
│   │   └── config.py
│   ├── models/
│   └── services/
├── .env
├── requirements.txt
└── README.md
```

---

## ⚙️ Instalación y configuración

### 1️⃣ Clonar el repositorio

```bash
git clone https://github.com/Andres-ann/prediction_service.git
cd prediction_service
```

---

### 2️⃣ Crear y activar entorno virtual

```bash
python3 -m venv venv
source venv/bin/activate
```

---

### 3️⃣ Instalar dependencias

```bash
pip install -r requirements.txt
```

> 📌 Si ves un error con `BaseSettings`, asegurate de tener instalado:
>
> ```bash
> pip install pydantic-settings
> ```

---

### 4️⃣ Configurar variables de entorno

Crear un archivo `.env` en la raíz del proyecto:

```bash
APP_NAME=PredictionService
APP_VERSION=1.0.0
DATABASE_URL=postgresql+psycopg2://user:password@localhost:5432/prediction_db
ENV=development
```

Estas variables permiten modificar la configuración sin cambiar el código fuente.

---

## 🧩 Ejecutar la aplicación

Desde la raíz del proyecto:

```bash
uvicorn app.main:app --reload
```

Si todo está correcto, verás algo como:

```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete.
```

---

## 📘 Documentación automática

FastAPI genera documentación Swagger y ReDoc automáticamente:

- 📄 **Swagger UI:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- 📘 **ReDoc:** [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

Ambas permiten probar los endpoints desde el navegador.

---

## 🪪 Licencia

MIT License © 2025  
Trabajo académico para la cátedra **Programación de Vanguardia** – Universidad de la Ciudad de Buenos Aires.
