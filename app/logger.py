import logging

def get_logger(name):
    # Create a logger with the given name
    logger = logging.getLogger(name)

    # Set the log level to INFO
    logger.setLevel(logging.INFO)

    # Create a console handler and set its level to INFO
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)

    # Create a formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # Add the formatter to the console handler
    ch.setFormatter(formatter)

    # Add the console handler to the logger
    logger.addHandler(ch)

    return logger