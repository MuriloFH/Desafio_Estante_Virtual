from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# criando a url da base
SQLALCHEMY_DATABASE_URL = "sqlite:///./olimpiadas.db"

# criando a engine para ser utilizada no projeto
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

# criando uma sessão da conexão realizada
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# criando uma base 
Base = declarative_base()