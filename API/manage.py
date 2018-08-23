import os
import unittest

# class for handling a set of commands
from flask_script import Manager

from app import db, create_app

# initialize the app with all its configurations
app = create_app(config_name=os.getenv('APP_SETTINGS'))

manager = Manager(app)

@manager.command
def test():
    """Runs the unit tests without test coverage."""
    tests = unittest.TestLoader().discover('app/tests', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1

if __name__ == '__main__':
    manager.run()