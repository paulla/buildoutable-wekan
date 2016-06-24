# -*- coding: utf-8 -*-
import ConfigParser
import socket

from subprocess import Popen as subprocess_Popen
from pymongo import MongoClient as pymongo_MongoClient
from os import getcwd as os_getcwd
from os.path import join as os_path_join
from time import sleep as time_sleep

from sys import (
    stderr as sys_stderr,
    exit as sys_exit,
)


config = ConfigParser.ConfigParser()
with open('buildout.cfg') as conf:
    config.readfp(conf)
    bind_ip = config.get('mongodb','bind_ip')
    port = config.get('mongodb','port')
    mongodb_data_path = config.get('mongodb','dbpath')
    mongodb_log_path = config.get('mongodb','logpath')

path_cwd = os_getcwd()

# need to fix : all options from rod.recipe.mongodb are not handle
mongod_proc = subprocess_Popen([
    os_path_join(path_cwd, 'bin/mongod'),
    '--dbpath', os_path_join(path_cwd,mongodb_data_path.split('/',1)[1]),
    '--bind_ip', bind_ip,
    '--master',
    '--port', port,
    '--logpath', os_path_join(path_cwd,mongodb_log_path.split('/',1)[1]),
    '--directoryperdb',
])

time_sleep(3)
print "Process ID of MongoD %s" % mongod_proc.pid

mongo_running = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
result = mongo_running.connect_ex((bind_ip, int(port)))

if result == 0:
    client = pymongo_MongoClient(bind_ip, int(port))
    db = client.wekan.add_user(
        'wekan',
        'wekan',
        roles=[
            {'role':"readWrite", 'db':"wekan"}
        ]
    )
else:
    sys_stderr.write('MongoDb not running : Fail to create "wekan" stuff\n')

mongod_proc.terminate()
if mongod_proc.wait() == 0:
    sys_stderr.write('MongoDb : setup "wekan" stuff successful\n')
