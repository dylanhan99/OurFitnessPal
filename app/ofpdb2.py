from sqlalchemy import create_engine, text, MetaData, Table, Column, Integer, String, inspect
from sqlalchemy.exc import SQLAlchemyError
from typing import Dict, List, Any, Optional, Union, Tuple
import logging

class SQLAlchemyWrapper:
    def __init__(self, connection_string: str):
        """
        Initialize the SQLAlchemy engine with the provided connection string.
        
        Args:
            connection_string: Database connection string (e.g., 'sqlite:///database.db')
        """
        self.engine = create_engine(connection_string)
        self.metadata = MetaData()
        self.tables = {}
        self.logger = logging.getLogger(__name__)
        
    def connect(self) -> None:
        """Establish a connection and load table metadata."""
        try:
            self.metadata.reflect(bind=self.engine)
            self.logger.info("Successfully connected to database")
        except SQLAlchemyError as e:
            self.logger.error(f"Error connecting to database: {str(e)}")
            raise
            
    def execute_query(self, query: str, params: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """
        Execute a raw SQL query and return the results.
        
        Args:
            query: SQL query string
            params: Parameters to bind to the query
            
        Returns:
            List of dictionaries containing the query results
        """
        try:
            with self.engine.connect() as connection:
                result = connection.execute(text(query), params or {})
                return [dict(row) for row in result]
        except SQLAlchemyError as e:
            self.logger.error(f"Error executing query: {str(e)}")
            raise
    
    def execute_with_commit(self, query: str, params: Optional[Dict[str, Any]] = None) -> int:
        """
        Execute a query that requires committing (INSERT, UPDATE, DELETE).
        
        Args:
            query: SQL query string
            params: Parameters to bind to the query
            
        Returns:
            Number of rows affected
        """
        try:
            with self.engine.begin() as connection:
                result = connection.execute(text(query), params or {})
                return result.rowcount
        except SQLAlchemyError as e:
            self.logger.error(f"Error executing query with commit: {str(e)}")
            raise
    
    def register_table(self, table_name: str, table_class: Any) -> None:
        """
        Register a custom table class with the wrapper.
        
        Args:
            table_name: Name of the table in the database
            table_class: Custom table class to associate with this table
        """
        if table_name not in self.metadata.tables:
            self.logger.warning(f"Table {table_name} not found in database metadata")
        
        self.tables[table_name] = table_class(self, table_name)
        self.logger.info(f"Registered table {table_name}")
    
    def get_table(self, table_name: str) -> Any:
        """
        Get the custom table object for a given table name.
        
        Args:
            table_name: Name of the table
            
        Returns:
            Custom table object
        """
        if table_name not in self.tables:
            raise ValueError(f"Table {table_name} is not registered")
        
        return self.tables[table_name]


class BaseTable:
    def __init__(self, db_wrapper: SQLAlchemyWrapper, table_name: str):
        """
        Initialize a table wrapper.
        
        Args:
            db_wrapper: SQLAlchemyWrapper instance
            table_name: Name of the table in the database
        """
        self.db = db_wrapper
        self.table_name = table_name
        self.logger = logging.getLogger(f"{__name__}.{table_name}")
        
        # Get SQLAlchemy Table object if it exists in metadata
        self.table = None
        if table_name in self.db.metadata.tables:
            self.table = self.db.metadata.tables[table_name]
    
    def get_column_names(self) -> List[str]:
        """Get the names of all columns in the table."""
        if not self.table:
            # Use inspector if table object is not available
            inspector = inspect(self.db.engine)
            return [col['name'] for col in inspector.get_columns(self.table_name)]
        
        return [column.name for column in self.table.columns]
    
    def get_primary_key(self) -> List[str]:
        """Get the names of primary key columns."""
        if not self.table:
            inspector = inspect(self.db.engine)
            pk_constraint = inspector.get_pk_constraint(self.table_name)
            return pk_constraint.get('constrained_columns', [])
            
        return [key.name for key in self.table.primary_key]
    
    def get_all_rows(self) -> List[Dict[str, Any]]:
        """Get all rows from the table."""
        query = f"SELECT * FROM {self.table_name}"
        return self.db.execute_query(query)
    
    def insert(self, data: Dict[str, Any]) -> int:
        """
        Insert a new row into the table.
        
        Args:
            data: Dictionary mapping column names to values
            
        Returns:
            ID of the inserted row or number of rows affected
        """
        columns = ", ".join(data.keys())
        placeholders = ", ".join(f":{key}" for key in data.keys())
        
        query = f"INSERT INTO {self.table_name} ({columns}) VALUES ({placeholders})"
        return self.db.execute_with_commit(query, data)
    
    def update(self, data: Dict[str, Any], condition: str, params: Optional[Dict[str, Any]] = None) -> int:
        """
        Update rows in the table.
        
        Args:
            data: Dictionary mapping column names to new values
            condition: WHERE clause for the update
            params: Parameters for the condition
            
        Returns:
            Number of rows affected
        """
        set_clause = ", ".join(f"{key} = :{key}" for key in data.keys())
        query = f"UPDATE {self.table_name} SET {set_clause} WHERE {condition}"
        
        # Merge data and params dictionaries
        all_params = {**data}
        if params:
            all_params.update(params)
            
        return self.db.execute_with_commit(query, all_params)
    
    def delete(self, condition: str, params: Optional[Dict[str, Any]] = None) -> int:
        """
        Delete rows from the table.
        
        Args:
            condition: WHERE clause for the delete
            params: Parameters for the condition
            
        Returns:
            Number of rows affected
        """
        query = f"DELETE FROM {self.table_name} WHERE {condition}"
        return self.db.execute_with_commit(query, params)


class UsersTable(BaseTable):
    """Custom implementation for the Users table."""
    
    def get_user_by_id(self, user_id: int) -> Optional[Dict[str, Any]]:
        """Get a user by their ID."""
        query = f"SELECT * FROM {self.table_name} WHERE id = :user_id LIMIT 1"
        results = self.db.execute_query(query, {"user_id": user_id})
        return results[0] if results else None
    
    def get_users_by_role(self, role: str) -> List[Dict[str, Any]]:
        """Get all users with a specific role."""
        query = f"SELECT * FROM {self.table_name} WHERE role = :role"
        return self.db.execute_query(query, {"role": role})
    
    def authenticate_user(self, username: str, password_hash: str) -> Optional[Dict[str, Any]]:
        """Authenticate a user by username and password hash."""
        query = f"""
            SELECT * FROM {self.table_name} 
            WHERE username = :username AND password_hash = :password_hash
            LIMIT 1
        """
        results = self.db.execute_query(query, {
            "username": username,
            "password_hash": password_hash
        })
        return results[0] if results else None


class FoodTable(BaseTable):
    """Custom implementation for the Food table."""
    
    def get_food_by_id(self, food_id: int) -> Optional[Dict[str, Any]]:
        """Get a food item by its ID."""
        query = f"SELECT * FROM {self.table_name} WHERE id = :food_id LIMIT 1"
        results = self.db.execute_query(query, {"food_id": food_id})
        return results[0] if results else None
    
    def get_foods_by_category(self, category: str) -> List[Dict[str, Any]]:
        """Get all food items in a specific category."""
        query = f"SELECT * FROM {self.table_name} WHERE category = :category"
        return self.db.execute_query(query, {"category": category})
    
    def get_foods_in_price_range(self, min_price: float, max_price: float) -> List[Dict[str, Any]]:
        """Get all food items within a specific price range."""
        query = f"""
            SELECT * FROM {self.table_name} 
            WHERE price >= :min_price AND price <= :max_price
            ORDER BY price ASC
        """
        return self.db.execute_query(query, {
            "min_price": min_price,
            "max_price": max_price
        })


# Example usage
def example_usage():
    # Initialize the wrapper
    db = SQLAlchemyWrapper('sqlite:///restaurant.db')
    db.connect()
    
    # Register custom table types
    db.register_table("users", UsersTable)
    db.register_table("food", FoodTable)
    
    # Get table instances
    users_table = db.get_table("users")
    food_table = db.get_table("food")
    
    # Use table-specific methods
    admin_users = users_table.get_users_by_role("admin")
    desserts = food_table.get_foods_by_category("dessert")
    
    # Generic query execution
    result = db.execute_query("SELECT * FROM users JOIN food ON users.favorite_food_id = food.id")
    
    # Insert new user
    new_user = {
        "username": "john_doe",
        "email": "john@example.com",
        "password_hash": "hashed_password_here",
        "role": "customer"
    }
    users_table.insert(new_user)
    
    # Update food prices
    food_table.update(
        {"price": 12.99}, 
        "category = :category AND price < :old_price",
        {"category": "main", "old_price": 10.00}
    )