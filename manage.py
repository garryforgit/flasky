# coding:utf8
# !/usr/bin/env python
# now you can run this py.file by ./manage.py (shebug define this)

import os
from app import create_app, db
from app.models import User, Role, Permission, Post
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)


def make_shell_context():
    return dict(app=app, db=db, User=User, Role=Role, Permission=Permission
                , Post=Post)


manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)  # add db-migrate command


@manager.command  # this decorator set the dunction_name as the command name
def test():  # you can use test command in the flask_script
    '''run the unit tests.'''
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)

@manager.command
def deploy():
    """Run deployment task."""
    from flask_migrate import upgrade
    from app.models import Role, User

    upgrade()

    # create new role
    Role.insert_roles()

    # let everybody follow the uper role
    User.add_self_follows()


if __name__ == '__main__':
    manager.run()
