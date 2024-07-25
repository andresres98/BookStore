from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, text

SQLALCHEMY_DATABASE_URL = "mysql+mysqlconnector://root:password123@localhost:3306/bookstore_api"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def test_connection():
    try:
        with SessionLocal() as session:
            result = session.execute(text("SELECT VERSION()"))
            version = result.fetchone()
            print(f"Conexión exitosa. Versión de MySQL: {version[0]}")
    except Exception as e:
        print(f"Error al conectar a la base de datos: {e}")

test_connection()