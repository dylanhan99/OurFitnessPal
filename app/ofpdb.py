from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError

db_engine = None

def init():
    global db_engine
    db_engine = create_engine("sqlite:///ofp.db")

def execute_sql_query(query):
    try:
        with db_engine.connect() as connection:
            result = connection.execute(text(query))
            return True, result.fetchall()
    except SQLAlchemyError as e:
        return False, str(e)