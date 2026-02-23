from app import db  
from flask_login import UserMixin
from datetime import datetime


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(150), unique = True, nullable = False)
    email = db.Column(db.String(150), unique = True, nullable = False)
    password = db.Column(db.String(200), nullable = False)

    tasks = db.relationship("Task", backref="author", lazy = True)

    def __repr__(self):
        return f"<User {self.username}>"

class Task(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(200),nullable = False)
    description = db.Column(db.Text, nullable = True)
    completed = db.Column(db.Boolean, default = False)
    created_at = db.Column(db.DateTime, default = datetime.now)

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"),nullable = False)

    def __repr__(self):
        return f"<Task {self.title}>"