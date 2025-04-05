from flask import current_app, Blueprint, render_template, request, session
import logging
from app import db_engine as db
from app import global_storage

blueprint_dev = Blueprint("dev", __name__)

def set_selected_table(table_name: str):
    try:
        selected_table = db.get_table(table_name)
        global_storage.set("selected_table_name", selected_table)
        result = db.execute_query(selected_table.select())
        print(result)
    except Exception as e:
        logging.error(str(e))

def render_dev():
    return render_template('dev.html', \
                            public_ipv4 = global_storage.get("IPV4_PUBLIC"), \
                            selected_table_name = global_storage.get("selected_table_name"), \
                            table_names = [name for name, _ in db.metadata.tables.items()] \
                            #table_ddl=session.get("table_ddl", []), \
                            #selected_table_name=session.get("selected_table_name", "-"), \
                            #selected_table_col_names=session.get("selected_table_col_names", None), \
                            #selected_table_data=session.get("selected_table_data", None), \
                            #query_err_msg=session.get("query_err_msg", "") \
                        )

@blueprint_dev.route("/dev", methods=['GET', 'POST'])
def dev_index():
    if request.method == 'GET': # First load
        db.get_table("Food").insert_food("celery", "tastes good", 12, 0, 1)

        # Just get the first tablename if there is one
        items = db.metadata.tables.items()
        print(items)
        if items and len(items) > 0:
            set_selected_table(list(items)[0][0]) # first tuple, first var
    elif request.method == 'POST':
        form = request.form
        form_id = form.get("form_id")
        if form_id == "choose_table":
            table_name = form["table_ddl"]
            set_selected_table(table_name)


    return render_dev()