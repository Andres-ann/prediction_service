# 🧠 Microservicio de Predicción de Reservas

Este proyecto forma parte del **Trabajo Práctico de la materia: Programación de Vanguardia 2025**.  
Su objetivo es desarrollar un **microservicio escalable** en **Python (FastAPI)** que formará parte de una plataforma de gestión de reservas, incorporando en el futuro un módulo de **predicción de demanda**.

---

# 🎯 Objetivo del microservicio

Proveer endpoints de predicción y análisis sobre la demanda de reservas (de salas, artículos, y patrones de uso) a partir del historial almacenado en la base de datos.

El microservicio se conecta a una base de datos (MySQL en XAMPP o PostgreSQL si se configura), la cual contiene información histórica proveniente de una API externa.
A partir de estos datos, se entrenan o aplican modelos analíticos ligeros para estimar tendencias y generar recomendaciones.

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
DATABASE_URL=mysql+pymysql://user:password@localhost:3306/predictions
ADMIN_DATABASE_URL= mysql+pymysql://user:password@localhost:3306/
EXTERNAL_API_URL=http://example.com
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
