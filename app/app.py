from flask import Flask, render_template, redirect, url_for
import requests
import sqlite3
#from flask_sqlalchemy import SQLAlchemy
#from sqlalchemy import inspect

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

# Database connection details
#app.config['SQLALCHEMY_DATABASE_URI'] = (
#    'mssql+pymssql://dylantheadmin:Test!1234@csd3156-dylancloud.database.windows.net/SampleDB'
#)
#app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#
#db = SQLAlchemy(app)

@app.route('/')
def index():
#    try:
#        inspector = inspect(db.engine)
#        table_data = {}
#
#        table_data = inspector.get_table_names()
#        
#        #for table_name in inspector.get_table_names():
#        #    query = f"SELECT * FROM {table_name}"
#        #    result = db.session.execute(query).fetchall()
#        #    table_data[table_name] = [dict(zip(row.keys(), row)) for row in result]
#        
#        return render_template('index.html', table_data=table_data)
#    except Exception as e:
#        return f"Error: {str(e)}"
    #{% for table_name in table_data %}
    #<p>{{table_name}}</p>
    #{% endfor %}

    return redirect(url_for("meals"))
    #return render_template('meals.html', public_ipv4=public_ipv4)

@app.route('/meals')
def meals(): 
    return render_template('meals.html', public_ipv4=public_ipv4)

@app.route('/dev')
def dev(): 
    return render_template('dev.html', public_ipv4=public_ipv4)

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
