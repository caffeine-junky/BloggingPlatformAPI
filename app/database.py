from typing import Generator, Annotated
from sqlmodel import SQLModel, Session, create_engine
from sqlalchemy import Engine
from loguru import logger
from fastapi import Depends


class Database:

    engine: Engine | None = None

    @classmethod
    def connect(cls, url: str) -> None:
        """"""
        if cls.engine:
            return
        try:
            cls.engine = create_engine(url, echo=True)
            logger.success("Connected to the database")
        except Exception as e:
            logger.critical(f"Failed to connect to the database: {e}")
    
    @classmethod
    def disconnect(cls) -> None:
        """"""
        if not cls.engine:
            return
        try:
            cls.engine.dispose()
            logger.success("Disconnected from the database")
        except Exception as e:
            logger.error(f"Failed to disconnect from the database: {e}")
        finally:
            cls.engine = None
    
    @classmethod
    def initialize(cls) -> None:
        """"""
        if not cls.engine:
            raise RuntimeError("Cannot initialize. Database not connected.")
        SQLModel.metadata.create_all(cls.engine)
    
    @classmethod
    def get_session(cls) -> Generator[Session, None, None]:
        """"""
        if not cls.engine:
            raise RuntimeError("Cannot get session. Database not connected.")
        with Session(cls.engine) as session:
            yield session


SessionDep = Annotated[Session, Depends(Database.get_session)]
