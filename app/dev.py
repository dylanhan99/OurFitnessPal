from flask import current_app, Blueprint, render_template, request, session

# My helpers
import random_helpers as ofp
import ofpdb

blueprint_dev = Blueprint("dev", __name__)

def set_selected_table(table_name: str):
    selected_table = ofpdb.get_table(table_name)
    if selected_table is None:
        session["selected_table_name"] = "-"
        session["selected_table_col_names"] = None
        session["selected_table_data"] = None
        return False, "ofpdb Failed to get_table"
    
    succ, result = ofpdb.execute_sql_query(selected_table.select())
    if not succ:
        session["selected_table_name"] = "-"
        session["selected_table_col_names"] = None
        session["selected_table_data"] = None
        return False, f"ofpdb Failed to execute_sql_query '{result}'"
    
    keys = [column.name for column in selected_table.columns]
    print (result)
    rows = [dict(row) for row in result]
    session["selected_table_name"] = table_name
    session["selected_table_col_names"] = keys
    session["selected_table_data"] = rows
    return True, ""

def render_dev():
    return render_template('dev.html', \
                            public_ipv4=current_app.config["IPV4_PUBLIC"], \
                            table_ddl=session.get("table_ddl", []), \
                            selected_table_name=session.get("selected_table_name", "-"), \
                            selected_table_col_names=session.get("selected_table_col_names", None), \
                            selected_table_data=session.get("selected_table_data", None), \
                            query_err_msg=session.get("query_err_msg", "") \
                        )

@blueprint_dev.route("/dev", methods=['GET'])
def dev_index():
    query = "SELECT name FROM sqlite_master WHERE type='table'"
    succ, sql_table_names = ofpdb.execute_sql_query(query)
    
    print(f"sql_table_names > {sql_table_names}")
    session["table_ddl"] = [row[0] for row in sql_table_names] if succ else []

    return render_dev()

@blueprint_dev.route("/dev", methods=['POST'])
def dev_submit():
    if request.method == 'POST':
        form_id = request.form.get("form_id")
        if form_id == "choose_table":
            table_name = request.form["table_ddl"]
            select_ok, err_msg = set_selected_table(table_name)
            if not select_ok:
                print(f"DEV - Failed to get {table_name} from ofdb > '{err_msg}'")
            
        elif form_id == "submit_query":
            query = request.form["query"]
            if len(query) > 0:
                succ, sql_value = ofpdb.execute_sql_query(query)
                session["query_err_msg"] = sql_value if not succ else ""
                # not doing anything with a "correct" return value rn
    
    return render_dev()