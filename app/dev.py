from flask import current_app, Blueprint, render_template, request, session
import logging
from app import db_engine as db
from app import global_storage

blueprint_dev = Blueprint("dev", __name__)

def set_selected_table(table_name: str):
    try:
        global global_storage
        global_storage.set("selected_table_name", table_name)
        #result = db.execute_query(selected_table.select())
        #print(result)
    except Exception as e:
        logging.error(str(e))

def erase_table_row(row_num: int):
    print(f"try to delete{row_num}")

    selected_table = db.get_table(global_storage.get("selected_table_name"))
    if selected_table:
        selected_table.erase_row(row_num)

def render_dev():
    global global_storage
    selected_table_name = global_storage.get("selected_table_name")
    selected_table = db.get_table(selected_table_name)
    column_names = [column.key for column in selected_table.db_type.__table__.columns] if selected_table else []
    select_all = selected_table.select_all()

    return render_template('dev.html', \
                            public_ipv4 = global_storage.get("IPV4_PUBLIC"), \
                            selected_table = selected_table, \
                            selected_table_name = selected_table_name, \
                            table_names = [name for name, _ in db.metadata.tables.items()], \
                            column_names = column_names, \
                            select_all = select_all \
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
        tables = db.metadata.tables
        if tables:
            items = list(tables.items())
            if len(items):
                set_selected_table(list(items)[0][0])
    elif request.method == 'POST':
        form = request.form
        form_id = form.get("form_id")
        if form_id == "choose_table":
            table_name = form["table_ddl"]
            set_selected_table(table_name)

        elif form_id == "delete_row":
            erase_table_row(int(form["row_num"]))

    return render_dev()