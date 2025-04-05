from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from flask_sqlalchemy import SQLAlchemy
from typing import Dict, List, Any, Optional, Union, Tuple
import logging
from threading import Lock
from abc import ABC, abstractmethod
from typing import Callable

db = SQLAlchemy() # Initialize empty thing so that db models can be set up

class DBEngine():
    """ A wrapper around the SQLAlchemy engine."""
    _engine = None

    def __init__(self):
        """
        Initialize the SQLAlchemy engine
        """
        self._engine = db
        self._tables = {}
        self._logger = logging.getLogger(__name__)
        self._lock = Lock()

    def execute_orm(self, obj: Any):
        try:
            session = self._engine.session
            return session.execute(obj).scalars()
        except SQLAlchemyError as e:
            self._logger.error(f"Error executing ORM: {str(e)}")
            raise

    def execute_with_commit(self, action: Callable[[Session], None]):
        """
        Execute given an ORM object
        """
        try:
            session = self._engine.session
            action(session)
            session.commit()
        except SQLAlchemyError as e:
            self._logger.error(f"Error executing ORM: {str(e)}")
            raise

    def register_table(self, table_name: str, table_class: Any) -> None:
        """
        Register an instance of custom table class to the db wrapper cache.
        table_class requires the class ctor to take in DBEngine class as param0
        """
        if (table_name in self._tables):
            self._logger.warning(f"Table {table_name} already in cache. Skipping...")
            return
        
        self._logger.warning(f"Table {table_name} not found in cache. Inserting...")
        self._tables[table_name] = table_class(self, table_name) # DBEngine as param0
        self._logger.info(f"Registered {table_name}")

    def get_table(self, table_name: str) -> Any:
        """
        Try to get table in cache.
        Throws an exception if not found.
        """
        if (table_name not in self._tables):
            #return None
            raise ValueError(f"Table {table_name} not registered")
        return self._tables[table_name]
        
    @property
    def db(self):
        return self._engine
    
    @property
    def metadata(self):
        return self._engine.metadata
    
    @property
    def tables(self):
        return self._tables

class BaseTable(ABC):
    '''
    Abstract Base Class (ABC) used for pure virtual functions
    '''
    def __init__(self, db_engine: DBEngine, table_name: str):
        self._db = db_engine
        self._table_name = table_name
        self._logger = logging.getLogger(f"{__name__}.{table_name}")
        
        self._table = None
        if self._table_name in self._db.metadata.tables:
            self._table = self._db.metadata.tables[self._table_name]

    @abstractmethod
    def select_all(self):
        pass
    
    @property
    def engine(self):
        return self._db

    @property
    def db(self):
        return self.engine.db
    
    @property
    def table_name(self):
        return self._table_name