from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

Base = declarative_base()
_engine = None
SessionLocal = None


def init_db(url: str):
    global _engine, SessionLocal
    _engine = create_engine(url, echo=False, future=True)
    SessionLocal = sessionmaker(bind=_engine)
    Base.metadata.create_all(_engine)


def get_session():
    if SessionLocal is None:
        raise RuntimeError("DB not initialized")
    return SessionLocal()
