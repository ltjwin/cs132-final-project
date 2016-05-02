from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.migrate import Migrate, MigrateCommand
from flask.ext.script import Manager

app = Flask(__name__)
app.config.from_object('finalProject.default_settings')
manager = Manager(app)



db = SQLAlchemy(app)
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)

from finalProject.models import *

@app.route("/")
def hello():
    return "Hello World!"

