from flask import current_app, Blueprint, render_template, request

# My helpers
import ofpdb

blueprint_dev = Blueprint("dev", __name__)

@blueprint_dev.route("/dev")
def dev_index():
    return render_template('dev.html', public_ipv4=current_app.config["IPV4_PUBLIC"], query_err_msg="")

@blueprint_dev.route("/dev", methods=['POST'])
def dev_post():
    query = request.form["query"]
    succ, sql_value = ofpdb.execute_sql_query(query)
    if succ:
        return render_template('dev.html', public_ipv4=current_app.config["IPV4_PUBLIC"], query_err_msg="")
    else:
        return render_template('dev.html', public_ipv4=current_app.config["IPV4_PUBLIC"], query_err_msg=sql_value)
