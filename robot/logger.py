import logging

def log_handler(level=None, name=None):
    """
    args:
        level:  logging level
    """

    FileLocation = 'logs/error.log'
    Formatter = logging.Formatter('%(asctime)s - %(name)s -> %(message)s')
    
    handler = logging.FileHandler(FileLocation)
    handler.setFormatter(Formatter)
    
    logger = logging.getLogger(__name__ if name == None else name)
    if level == None:
        logger.setLevel(logging.INFO)
    logger.addHandler(handler)

    return logger
