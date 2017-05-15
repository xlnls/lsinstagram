# -*-encoding=UTF-8 -*-

from lsinstagram import app
from flask_script import Manager

manager = Manager(app)

if __name__=='__main__':
    manager.run()
