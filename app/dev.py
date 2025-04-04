from flask import current_app, Blueprint, render_template, request, session
from flask_login import login_required

# My helpers
import random_helpers as ofp
#from ofpdb import DBEngine
from app import db

blueprint_dev = Blueprint("dev", __name__)

def set_selected_table(table_name: str):
    try:
        selected_table = db.get_table(table_name)
        result = db.execute_query(selected_table.select())
        print(result)
    except:
        return

def render_dev():
    return render_template('dev.html') #\
                            #public_ipv4=OFPGlobals().get("IPV4_PUBLIC"), \
                            #table_ddl=session.get("table_ddl", []), \
                            #selected_table_name=session.get("selected_table_name", "-"), \
                            #selected_table_col_names=session.get("selected_table_col_names", None), \
                            #selected_table_data=session.get("selected_table_data", None), \
                            #query_err_msg=session.get("query_err_msg", "") \
                        #)

@blueprint_dev.route("/dev", methods=['GET'])
@login_required
def dev_index():
    query = "SELECT name FROM sqlite_master WHERE type='table'"
    #result = db.execute_query(query)
    #print (result)

    return render_dev()

@blueprint_dev.route("/dev", methods=['POST'])
@login_required
def dev_submit():
    
    
    return render_dev()