from loguru import logger
from datetime import datetime


def init(name):
    """
    Function that create a logger instance for the problem that will track all
    information, debug and errors messages in a log file

    Parameters
    ----------
    name : name of the application initiating the logger
    """

    now = datetime.now()
    filename = "logs/{0}_{1}.log".format(name, now.strftime("%m_%d_%y"))
    logger.remove()  # remove stderr messages (so it doesn't mess up ncruses)
    # New file is created each day at noon
    logger.add(
            filename,
            rotation="00:00",
            format="<green>{time}</green> <level>{message}</level>"
            )


def enableRetention():
    """
    Function that enables a log file assignment for each day period. Logs that
    are older than 10 days are archived.
    """
    logger.add("file_X.log", retention="10 days")  # Cleanup after 10 day s
    logger.add("file_Y.log", compression="zip")    # Compress history
