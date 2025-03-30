from flask import Flask, render_template, redirect, url_for

# My helpers
import random_helpers as ofp
import ofpdb

# My Py pages
from dev import blueprint_dev

def create_app():
    app = Flask(__name__) # Get anywhere via current_app
    app.secret_key = "some_key"

    @app.route('/')
    def index():
        return redirect(url_for("dev.dev_index"))

    @app.route('/meals')
    def meals(): 
        return render_template('meals.html', public_ipv4=app.config["IPV4_PUBLIC"])

    # Page blueprints
    app.register_blueprint(blueprint_dev)
        
    # Global vars
    app.config["IPV4_PUBLIC"] = ofp.fetch_instance_ip()
    
    return app

if __name__ == '__main__':
    # one-off init stuff
    # Core init
    app = create_app()
    
    # System/Engine inits
    ofpdb.init()

    # entrypoint
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
