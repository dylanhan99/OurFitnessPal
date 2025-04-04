from flask import Flask, request, redirect, url_for, flash, Blueprint
from flask_login import LoginManager, login_manager, UserMixin, login_user, current_user, login_required, logout_user
from misc_tools import OFPStorage
from app import ofp_app, user_storage
from typing import Dict

users: Dict[str, bool] = {} # to use the database eventually

class User(UserMixin):
    def __init__(self, username):
        self.id = username
        
    def get_id(self):
        return self.id
    
blueprint_login = Blueprint("login", __name__)
    
@ofp_app.login_manager.user_loader
def load_user(username):
    print(f"load_user{username}")
    
    return User(username) if username in users else None

@blueprint_login.route("/logout")
def logout_index():
    logout_user()

    return redirect(url_for("login.login_index"))

@blueprint_login.route("/login", methods=['GET', 'POST'])
def login_index():
    if (request.method == 'POST'):
        username = request.form.get('username')
        if username:
            # Locate username in database
            
            # Register the user if they don't exist
            
            # Create a User object and log them in
            user = User(username)
            login_user(user)
            return redirect(url_for("dev.dev_index"))
            
            print("hello2222?")
            
            print(f"users > {users}")
            # Initialize storage for this user if needed
            if username not in users:
                users[username] = True
                print(f"created user {username}")
                global user_storage
                if username not in user_storage.keys(): # only recreate if not found
                    user_storage[username] = OFPStorage()
            else:
                print(f"could not create user {username}")

    return '''
        <form method="post">
            <input type="text" name="username" placeholder="Username">
            <button type="submit">Login</button>
        </form>
    '''
    