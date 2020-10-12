from loguru import logger
from datetime import datetime


def init(name):
    """
    Function that create a logger instance for the problem that will track all information, debug and errors messages in a log file
    Parameters
    ----------
    name : name of the application initiating the logger
    Returns
    -------
    None
    """
    now = datetime.now()
    filename = "/var/log/ultra{0}_{1}.log".format(name, now.strftime("%m_%d_%y"))
    logger.add(filename, rotation="00:00", format="<green>{time}</green> <level>{message}</level>") # New file is created each day at noon
    logger.warning("Logs will saved in logs/{0}_{1}.log".format(name, now.strftime("%m_%d_%y")))


def enableRetention():
    """
    Function that enables a log file assignment for each day period. Logs that are older than 10 days are archived.
    Parameters
    ----------
    None
    Returns
    -------
    None
    """
    logger.add("file_X.log", retention="10 days")  # Cleanup after 10 day s
    logger.add("file_Y.log", compression="zip")    # Compress history
