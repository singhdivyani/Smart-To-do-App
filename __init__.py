# for python model
from flask import Flask
from  flask_sqlalchemy import SQLAlchemy

# create database object globally
db=SQLAlchemy()
def create_app(): #create an return flask app
    app= Flask(__name__)
    app.secret_key='supersecretkey'
    # app.config['SECRET_KEY']='supersecretkey'
    # That connection string will not work as written because your MySQL password contains special characters (#, ?, $) that break the URI format.
# You need to URL-encode the password so SQLAlchemy reads it correctly. 
# password=Div#200_3?0$7
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:mypassword123@localhost/todoflask_app'


    app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
    
    db.init_app(app)   #for connecting db to  app
    # import blueprint to use
    from .routes.auth import auth_bp
    from .routes.task import task_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(task_bp)
    return app

    
