# login logout routes
from flask import Blueprint,render_template,redirect,url_for,request,flash,session
from PROJECT_FLASK import db
from PROJECT_FLASK.models.model import User
from werkzeug.security import generate_password_hash, check_password_hash
# __name__  This tells Flask where this blueprint’s code lives (its import name).
# Flask uses this to find resources like templates and static files relative to this file’s location.
# __name__ is just a Python built-in variable that holds the current module’s name.
# 'auth' This is the blueprint name
auth_bp=Blueprint('auth',__name__) #blueprint object creation 

# USER_CREDENTIALS={
#     'username':'admin',
#     'password':'1234'
# }
@auth_bp.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get('username').strip()
        password = request.form.get('password')

        if not username or not password:
            flash("Username and password are required", "danger")
            return redirect(url_for('auth.register'))

        # Check if username is already taken
        if User.query.filter_by(username=username).first():
            flash("Username already exists", "danger")
            return redirect(url_for('auth.register'))

        # Create new user
        new_user = User(username=username)
        new_user.password_hash = generate_password_hash(password)
        db.session.add(new_user)
        db.session.commit()

        flash("Registration successful! Please log in.", "success")
        return redirect(url_for('auth.login'))

    return render_template('register.html')
@auth_bp.route('/login',methods=["GET","POST"])
def login():
    if request.method=="POST":
        username=request.form.get('username').strip()
        password=request.form.get('password')
        user=User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password_hash,password):
            session['user_id']=user.id
            session['username']=user.username
            flash('login Successful !','success')
            return redirect(url_for('tasks.view_task'))
        else:
            flash('Invalid username or password','danger')
    return render_template('login.html')
@auth_bp.route('/logout')
def logout():
    session.pop('user_id',None)
    session.pop('user',None)
    flash('Logged out successfully','info')
    return redirect(url_for('auth.login'))

