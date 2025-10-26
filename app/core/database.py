from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.engine import make_url
import pymysql
from sqlalchemy.exc import OperationalError
from app.core.config import settings

Base = declarative_base()

def ensure_database_exists():
    """Crea la base de datos MySQL si no existe."""
    db_url = settings.database_url
    admin_url = settings.admin_database_url

    if not db_url:
        raise RuntimeError("DATABASE_URL is not set. Define the DATABASE_URL environment variable.")

    try:
        parsed = make_url(db_url)
        db_name = parsed.database
        if not db_name:
            raise RuntimeError("Could not extract database name from DATABASE_URL")
    except Exception as e:
        raise RuntimeError(f"Error parsing DATABASE_URL: {e}")

    if not admin_url:
        # Si no hay admin url, asumimos que no intentaremos crear la base (por ejemplo en entornos locales)
        print("ADMIN_DATABASE_URL not set: Assumes the database already exists or manual creation will be necessary.")
        return

    try:
        admin_engine = create_engine(admin_url)
        # Usar autocommit para sentencias CREATE DATABASE en MySQL
        with admin_engine.connect().execution_options(isolation_level="AUTOCOMMIT") as conn:
            result = conn.execute(
                text("SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA WHERE SCHEMA_NAME = :db"),
                {"db": db_name},
            )
            exists = result.first()
            if not exists:
                print(f"Creating database...")
                conn.execute(text(f"CREATE DATABASE {db_name}"))
                print(f"Database created.")
            else:
                print(f"Database already exists.")
    except OperationalError as e:
        print("Error connecting to MySQL (admin):", e)
        raise

def get_engine():
    ensure_database_exists()
    return create_engine(settings.database_url, echo=False, future=True)

# Crear engine y SessionLocal después de validar configuración
engine = get_engine()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    """Crea las tablas si no existen."""
    from app.schemas.history_schema import ReservationHistory
    print("Checking tables in the database")
    Base.metadata.create_all(bind=engine)
    print("Database and tables ready.")