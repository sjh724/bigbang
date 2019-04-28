# -*- coding:utf-8 -*-

from app import create_app, db
# from flask.ext.sqlalchemy import SQLAlchemy
from flask_script import Manager, Shell
from config import config

app = create_app("default")
manager = Manager(app)

def make_shell_context():
    return dict(app=app, db=db)

manager.add_command("shell", Shell(make_context=make_shell_context))

if __name__ == "__main__":
    manager.run()
