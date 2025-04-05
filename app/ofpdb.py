from sqlalchemy.exc import SQLAlchemyError
from flask_sqlalchemy import SQLAlchemy
from typing import Dict, List, Any, Optional, Union, Tuple
import logging
from threading import Lock

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
        self._logger = logging.getLogger(__name__) # i think shd make logger a global
        self._lock = Lock()

    def execute_query(self, query: str, params: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """
        Execute stringified SQL query and returns the results
        Params may be provided which binds to the query
        Returns dict containing query results
        """
        try:
            with self._engine.connect() as connection:
                result = connection.execute(query, params)
                return [dict(row) for row in result]
        except SQLAlchemyError as e:
            self._logger.error(f"Error executing query: {str(e)}")
            raise

    def execute_with_commit(self, query: str, params: Optional[Dict[str, Any]] = None) -> int:
        """
        Execute stringified SQL query and returns the results
        Params may be provided which binds to the query
        Returns number of rows altered
        """
        try:
            with self._engine.connect() as connection:
                result = connection.execute(query, params) # It will throw an error safely in cases of multi-line query
                connection.commit()
                return result.rowcount
        except SQLAlchemyError as e:
            self._logger.error(f"Error executing query: {str(e)}")
            raise

    def execute_with_commit(self, obj: Any):
        """
        Execute given an ORM object or query string
        """
        try:
            if (hasattr(obj, '__table__')):
                session = self._engine.session
                session.add(obj)
                session.commit()
                return obj
            else:
                return None
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

class BaseTable:
    def __init__(self, db_engine: DBEngine, table_name: str):
        self._db = db_engine
        self._table_name = table_name
        self._logger = logging.getLogger(f"{__name__}.{table_name}")
        
        self._table = None
        if self._table_name in self._db.metadata.tables:
            self._table = self._db.metadata.tables[self._table_name]

    def insert(self, data: Dict[str, Any]) -> int:
        columns = ", ".join(data.keys())
        placeholders = ", ".join(f":{key}" for key in data.keys())
        
        query = f"INSERT INTO {self._table_name} ({columns}) VALUES ({placeholders})"
        return self._db.execute_with_commit(query, data)

    def update(self, data: Dict[str, Any], condition: str, condition_data: Dict[str, Any] = None) -> int:
        placeholders = ", ".join(f"{key} = :{key}" for key in data.keys())
        all_data = {**data} # Copying data
        if condition_data:
            all_data.update(condition_data) # Appending other data

        query = f"UPDATE {self._table_name} SET ({placeholders}) WHERE ({condition})"
        return self._db.execute_with_commit(query, all_data)
    
    def delete(self, condition: str, condition_data: Dict[str, Any] = None) -> int:
        query = f"DELETE FROM {self._table_name} WHERE {condition}"
        return self._db.execute_with_commit(query, condition_data)