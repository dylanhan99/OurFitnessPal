from flask import redirect, url_for

if __name__ == '__main__':
    from app import init_app
    # Core init
    init_app() # app accessible via flask:current_app

    from app import ofp_app

    @ofp_app.route('/')
    def index():
        #return redirect(url_for("dev.dev_index"))
        return redirect(url_for("login.login_index"))

    from login import blueprint_login
    from dev import blueprint_dev

    #@app.route('/meals')
    #def meals(): 
    #    return render_template('meals.html', public_ipv4=OFPGlobals().get("IPV4_PUBLIC"))

    # Page blueprints
    #app.register_blueprint(blueprint_dev)
    ofp_app.register_blueprint(blueprint_login)
    ofp_app.register_blueprint(blueprint_dev)

    # entrypoint
    ofp_app.run(debug=True, host='0.0.0.0')

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
