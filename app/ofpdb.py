from sqlalchemy import Executable, create_engine, Table, MetaData, inspect, text
from sqlalchemy.exc import SQLAlchemyError

db_engine = None
db_metadata = None

def init():
    global db_engine
    global db_metadata
    db_engine = create_engine("sqlite:///ofp.db")
    db_metadata = MetaData()

def execute_sql_query(query):
    try:
        with db_engine.connect() as connection:
            if isinstance(query, Executable):
                result = connection.execute(query)
            elif isinstance(query, str):
                result = connection.execute(text(query))
            else:
                return False, "execute_sql_query - Query is neither a Executable nor a str"
            return True, result.fetchall()
    except SQLAlchemyError as e:
        return False, str(e)

# Returns a handle to the table. 
# Returns None if cannot find.    
def get_table(table_name: str):
    print(f"get_table - {table_name}")
    db_inspector = inspect(db_engine)
    if table_name not in db_inspector.get_table_names():
        return None
    return Table(table_name, db_metadata, autoload_with=db_engine)
