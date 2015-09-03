from utils.custom_logger import *
from settings.settings import *
import socket
import sys
import time

custom_logger = CustomLogger()

def get_lock(process_name):
    custom_logger.log(APP_LOCK)
    if(not APP_LOCK):
        custom_logger.log('APP_LOCK is False!!!')
        return

    global lock_socket
    lock_socket = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
    try:
        lock_socket.bind('\0' + process_name)
        custom_logger.log('App start working.')
    except socket.error:
        custom_logger.log('Another app can not start. Previous app is running.')
        sys.exit()
