import os
import logging
dir_path = os.path.dirname(os.path.abspath(__file__))

LOG_FILE = os.path.join(dir_path,"../out/app.log")
LOG_FORMAT = "%(asctime)s %(message)s"
LOG_DATE = "%m/%d/%Y %H:%M:%S"
LOG_LEVEL = logging.DEBUG
LOG_FILE_MAX_LINE = 15000
