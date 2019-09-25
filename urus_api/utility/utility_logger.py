# -*- coding: utf-8 -*-
# !/usr/bin/python
'''
We collect all utilities of logger module here, these include logger initilization and other function calls for other python scripts.
It's good to utilize the OO concept to avoid duplicated code everywhere.
'''
import os
import logging
from logging.handlers import TimedRotatingFileHandler

# pre-setting macro
log_to_console = False


def init_logger(filepath='spam.log'):
    # create formatter and add it to the handlers
    formatter = logging.Formatter(
        '%(asctime)s %(levelname)s (%(process)d) %(module)s/%(funcName)s():%(lineno)s - %(message)s'
    )

    # create file handler which logs even debug messages
    fh = logging.FileHandler(filepath)
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(formatter)

    # add the handlers to logger
    logger = logging.getLogger('r6_rcv_log')
    logger.setLevel(logging.DEBUG)
    logger.addHandler(fh)

    if log_to_console:
        # create console handler with a higher log level
        ch = logging.StreamHandler()
        ch.setLevel(logging.ERROR)
        ch.setFormatter(formatter)
        logger.addHandler(ch)

    return logger


def init_time_rotating_logger(filepath='time_rotating_log.log',
                              name='_shared_log'):
    # create formatter and add it to the handlers

    # log_format = '%(asctime)s - %(module)s - %(levelname)s - %(message)s'
    log_format = '%(asctime)s %(levelname)s (%(process)d) %(module)s/%(funcName)s():%(lineno)s - %(message)s'
    formatter = logging.Formatter(fmt=log_format, datefmt="%Y-%m-%d %H:%M:%S")

    # create timeRotating handler which logs even debug messages
    th = TimedRotatingFileHandler(
        filepath, when='midnight', interval=1, backupCount=7, encoding='utf8')
    th.setLevel(logging.DEBUG)
    th.setFormatter(formatter)
    th.suffix = "%Y-%m-%d"

    # add the handlers to logger
    logger = logging.getLogger(
        name
    )  # Multiple calls to getLogger() with the same name will always return a reference to the same Logger object.
    logger.setLevel(logging.DEBUG)
    logger.addHandler(th)

    return logger


log_path = os.getcwd() + "/logs/" + "urus.log"
logger = init_time_rotating_logger(log_path, 'log_urus')
print(f'log_path:[{log_path}]')
