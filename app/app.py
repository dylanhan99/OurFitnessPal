from typing import Dict, Any
from flask import Flask
from flask_login import LoginManager, login_manager
from flask_sqlalchemy import SQLAlchemy

from misc_tools import OFPStorage
import random_helpers as ofp

ofp_app = None # Get anywhere via current_app
#login_manager = None
db = None
user_storage = None
global_storage = None

def init_app():
    global ofp_app
    global db
    global login_manager
    global user_storage
    global global_storage
    
    ofp_app = Flask(__name__)
    ofp_app.secret_key = "yomama"
    ofp_app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///ofp.db"
    ofp_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    login_manager = LoginManager()
    login_manager.init_app(ofp_app)

    db = SQLAlchemy(ofp_app)

    user_storage = dict[str, OFPStorage]()
    
    global_storage = OFPStorage()
    global_storage.set("IPV4_PUBLIC", ofp.fetch_instance_ip())

    return ofp_app