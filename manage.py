from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from app.main import app, db
from app.models import *
import json


migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)


@manager.command
def initial_data(path):
    with open(path, 'r') as inital_file:
        data = json.load(inital_file)
    for item in data:
        raw = 'INSERT INTO {} ({}) VALUES ({});'.format(item['model'],
                                                        ', '.join(item['fields'].keys()),
                                                        ', '.join(["'{}'".format(item['fields'][k]) for k in item['fields'].keys()]))
        db.engine.execute(raw)


@manager.command
def create_admin(username, password):
    user = User(id=1,
                username=username,
                role_id=1)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()


@manager.command
def run():
    app.secret_key = SECRET_KEY
    app.run()


if __name__ == '__main__':
    manager.run()
