from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from core.config import get_settings
from core.logger import logger

settings = get_settings()
Base = declarative_base()

class Database:
    _instance = None
    _engine = None
    _SessionLocal = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        logger.info(f"Connecting to database: {settings.DATABASE_URL}")
        connect_args = {"check_same_thread": False} if settings.DATABASE_URL.startswith('sqlite') else {}
        
        self._engine = create_engine(
            settings.DATABASE_URL, 
            connect_args=connect_args
        )
        self._SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self._engine)
        Base.metadata.create_all(bind=self._engine)

    def get_session(self):
        db = self._SessionLocal()
        try:
            yield db
        finally:
            db.close()

    @property
    def engine(self):
        return self._engine