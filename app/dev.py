from flask import current_app, Blueprint, render_template, request, session

# My helpers
import ofpdb

blueprint_dev = Blueprint("dev", __name__)

def render_dev():
    return render_template('dev.html', \
                            public_ipv4=current_app.config["IPV4_PUBLIC"], \
                            table_combo=session.get("table_combo", []), \
                            query_err_msg=session.get("query_err_msg", ""), \
                            selected_table_name=session.get("selected_table_name", ""))

@blueprint_dev.route("/dev", methods=['GET'])
def dev_index():
    query = "SELECT name FROM sqlite_master WHERE type='table'"
    succ, sql_table_names = ofpdb.execute_sql_query(query)
    session["table_combo"] = [row[0] for row in sql_table_names] if succ else []

    return render_dev()

@blueprint_dev.route("/dev", methods=['POST'])
def dev_submit():
    if request.method == 'POST':
        form_id = request.form.get("form_id")
        print(form_id)
        if form_id == "choose_table":
            session["selected_table_name"] = request.form["table_ddl"]
            
        elif form_id == "submit_query":
            query = request.form["query"]
            if len(query) > 0:
                succ, sql_value = ofpdb.execute_sql_query(query)
                session["query_err_msg"] = sql_value if succ else ""
                # not doing anything with a "correct" return value rn
    
    return render_dev()