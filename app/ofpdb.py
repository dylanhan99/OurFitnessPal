from sqlalchemy import SQLAlchemy, create_engine, text, MetaData, Table, Column, Integer, String, inspect
from sqlalchemy.exc import SQLAlchemyError
from typing import Dict, List, Any, Optional, Union, Tuple
import logging
from threading import Lock

from misc_tools import BaseSingleton

db_engine = create_engine("sqlite:///ofp.db")
db = SQLAlchemy(db_engine)

class DBEngine(BaseSingleton):
    """ A wrapper around the SQLAlchemy engine."""
    _engine = db_engine

    #####
    # Some models for this engine
    class UserTable(db.Model):
        id          = db.Column(db.Integer, primary_key=True)
        username    = db.Column(db.String(20), unique=True, nullable=False)
        password    = db.Column(db.String(120), nullable=False)
    
    class FoodTable(db.Model):
        id          = db.Column(db.Integer, primary_key=True)
        name        = db.Column(db.String(80), nullable=False)
        description = db.Column(db.String(120), nullable=False)
        user_id     = db.Column(db.Integer, db.ForeignKey("UserTable.id"))
    #####

    def __init__(self):
        """
        Initialize the SQLAlchemy engine given a connection string
        e.g. 'sqlite:///ofp.db'
        """
        self._metadata = MetaData()
        self._tables = {}
        self._logger = logging.getLogger(__name__) # i think shd make logger a global
        self._lock = Lock()

    def connect(self) -> None:
        """
        To explicitly refresh metadata. Needed cus of loadbalancing, so all app servers
        are out of sync you could think of it. So gotta always refresh with main DB server stuff.
        """
        try:
            self._metadata.reflect(bind=self.engine)
            self._logger.info("Successfully connected to database")
        except SQLAlchemyError as e:
            self._logger.error(f"Error connecting to database: {str(e)}")
            raise

    def execute_query(self, query: str, params: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """
        Execute stringified SQL query and returns the results
        Params may be provided which binds to the query
        Returns dict containing query results
        """
        try:
            self.connect()
            with self._engine.connect() as connection:
                result = self.execute(query, params)
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
            self.connect()
            with self._engine.connect() as connection:
                result = self.execute(query, params) # It will throw an error safely in cases of multi-line query
                self.session.commit()
                return result.rowcount
        except SQLAlchemyError as e:
            self._logger.error(f"Error executing query: {str(e)}")
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
        return self._metadata
    
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
    
    
class FoodTable(BaseTable):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

#    
#
######################################################
#
#db_engine = None
#db_metadata = None
#
##CREATE TABLE users (id INT PRIMARY KEY, name VARCHAR(100), email VARCHAR(100));
#class User(db.Model):
#    id = db.Column(db.Integer, primary_key=True)
#    name = db.Column(db.String(80), nullable=False)
#    email = db.Column(db.String(120), unique=True, nullable=False)
#
#def init():
#    global db_engine
#    global db_metadata
#    db_engine = create_engine("sqlite:///ofp.db")
#    db_metadata = MetaData()
#
#def execute_sql_query(query):
#    try:
#        with db_engine.connect() as connection:
#            if isinstance(query, Executable):
#                result = connection.execute(query)
#            elif isinstance(query, str):
#                result = connection.execute(text(query))
#            else:
#                return False, "execute_sql_query - Query is neither a Executable nor a str"
#            return True, result.fetchall()
#    except SQLAlchemyError as e:
#        return False, str(e)
#
## Returns a handle to the table. 
## Returns None if cannot find.    
#def get_table(table_name: str):
#    print(f"get_table - {table_name}")
#    db_inspector = inspect(db_engine)
#    if table_name not in db_inspector.get_table_names():
#        return None
#    return Table(table_name, db_metadata, autoload_with=db_engine)
