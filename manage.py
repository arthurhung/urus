#! /usr/bin/env python3
from flask_script import Manager
from werkzeug.wsgi import DispatcherMiddleware
import socket

from urus_api import create_app
from urus_api.config import IDC, UAT, Develop

HOSTNAME = socket.gethostname()
if HOSTNAME == 'webapi-ss':
    config_obj = IDC
elif HOSTNAME == 'webapi-idc':
    config_obj = IDC
elif HOSTNAME == 'webapi-uat':
    config_obj = UAT
else:
    config_obj = Develop

app = create_app(config_obj)

manager = Manager(app)


# 自定指令
@manager.command
def hello():
    """Print hello"""
    print("hello!")


@manager.command
def runuwsgi(config_obj):
    pass


if __name__ == "__main__":
    manager.run()
