from typing import Dict, Any
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from misc_tools import OFPStorage
import random_helpers as ofp
from ofpdb import db, DBEngine

ofp_app = None # Get anywhere via current_app
db_engine: DBEngine = None # The wrapper aronud db
global_storage: OFPStorage = None # Opting to use this because sometimes my globals are not json-able, session cookies are not ideal

def init_app():
    global ofp_app
    global global_storage
    global db
    global db_engine
    
    ofp_app = Flask(__name__)
    ofp_app.secret_key = "yomama"

    username = "postgres"
    password = "password"
    endpoint = "ofp-postgres.cplyqbsys4o5.us-east-1.rds.amazonaws.com"
    db_name = "postgres"

    # mysql+pymysql://<username>:<password>@<endpoint>/<database_name>
    ofp_app.config["SQLALCHEMY_DATABASE_URI"] = \
        f"postgresql+psycopg2://{username}:{password}@{endpoint}/{db_name}"
    ofp_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(ofp_app)
    from db_classes import db_FoodTable, FoodTable

    # Need a external input to create tables or not
    # if True:
    with ofp_app.app_context():
        try:
            with db.engine.connect():
                print("Database connection successful!")
        except Exception as e:
            print(f"Database connection failed: {e}")
            return
        
        db.create_all()
        
        db_engine = DBEngine()
        db_engine.register_table(db_FoodTable().__tablename__, FoodTable)

        # Debug print all created tables
        tables = db_engine.metadata.tables
        if (tables):
            for name, obj in tables.items():
                print(f"\n* Table: {name}")
        else:
            print("no tables")

    global_storage = OFPStorage()
    global_storage.set("IPV4_PUBLIC", ofp.fetch_instance_ip())

    return ofp_app