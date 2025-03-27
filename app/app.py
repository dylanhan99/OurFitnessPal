from flask import Flask, render_template
#from flask_sqlalchemy import SQLAlchemy
#from sqlalchemy import inspect

app = Flask(__name__)

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

    message = "hi"
    return render_template('index.html', message=message)
    #<p>{{message}}</p>

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
