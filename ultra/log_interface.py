import sys
from loguru import logger
from datetime import datetime

def init(name):
    now = datetime.now()
    filename = "logs/{0}_{1}.log".format(name, now.strftime("%m_%d_%y"))
    logger.add(filename, rotation="00:00", format="<green>{time}</green> <level>{message}</level>") # New file is created each day at noon
    logger.warning("Logs will saved in logs/{0}_{1}.log".format(name, now.strftime("%m_%d_%y")))


def enableRetention():
        logger.add("file_X.log", retention="10 days")  # Cleanup after 10 day s
        logger.add("file_Y.log", compression="zip")    # Compress history
