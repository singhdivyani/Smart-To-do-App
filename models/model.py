# to represent table 
from PROJECT_FLASK import db
from werkzeug.security import generate_password_hash, check_password_hash
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
# relationship
    tasks=db.relationship('Task',backref='user',lazy=True)
# password handling
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
class Task(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    task_name=db.Column(db.String(100),nullable=False)
    status=db.Column(db.String(20),default="Pending")

    # foreign key linking to user
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)