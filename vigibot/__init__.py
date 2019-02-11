import logging
import os
from logging.handlers import TimedRotatingFileHandler

# start logging to the file with log rotation at midnight
logformatter = logging.Formatter('%(asctime)s %(name)s %(levelname)s %(message)s')
loghandler = TimedRotatingFileHandler(os.path.dirname(os.path.realpath(__file__)) + '/../tradebot.log',
                                   when='midnight',
                                   backupCount=10)
loghandler.setFormatter(logformatter)
