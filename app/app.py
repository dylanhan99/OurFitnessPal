from flask import Flask, render_template, redirect, url_for, request
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
import requests

app = Flask(__name__)
public_ipv4 = None

def fetch_instance_ip():
    global public_ipv4
    try:
        public_ipv4 = "Unable to retrieve public IP"
        #public_ipv4 = requests.get("http://169.254.169.254/latest/meta-data/public-ipv4").text
    except requests.RequestException:
        public_ipv4 = "Unable to retrieve public IP"

with app.app_context():
    fetch_instance_ip()

# Database engine details
db_engine = create_engine("sqlite:///ofp.db")

@app.route('/')
def index():
    return redirect(url_for("dev"))

@app.route('/meals')
def meals(): 
    return render_template('meals.html', public_ipv4=public_ipv4)

@app.route('/dev')
def dev(): 
    #connection.execute()
    return render_template('dev.html', public_ipv4=public_ipv4, query_err_msg="")

@app.route('/dev', methods=['POST'])
def dev_post():
    query = request.form["query"]
    succ, sql_value = execute_sql_query(query)
    if succ:
        return render_template('dev.html', public_ipv4=public_ipv4, query_err_msg="")
    else:
        return render_template('dev.html', public_ipv4=public_ipv4, query_err_msg=sql_value)

def execute_sql_query(query):
    try:
        with db_engine.connect() as connection:
            result = connection.execute(text(query))

            rows = result.fetchall()
            return True, rows
    except SQLAlchemyError as e:
        return False, str(e)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

#class User(db.Model):
#    __tablename__ = 'USER'
#    id = db.Column(db.Integer, primary_key=True)
#    name = db.Column(db.String(100), nullable=False)
#    email = db.Column(db.String(100), nullable=False)
#
#@app.route('/')
#def index():
#    try:
#        users = User.query.all()
#        return render_template('index.html', users=users)
#    except Exception as e:
#        return f"Error: {str(e)}"
#
#@app.route('/add_user', methods=['POST'])
#def add_user():
#    name = request.form.get('name')
#    email = request.form.get('email')
#    
#    try:
#        new_user = User(name=name, email=email)
#        db.session.add(new_user)
#        db.session.commit()
#        return "User added successfully!"
#    except Exception as e:
#        return f"Error: {str(e)}"
