import logging
import colorlog
import sys


def setup_logger(name=__name__, console_level=logging.INFO):
    main_logger = logging.getLogger(name)
    main_logger.setLevel(console_level)

    console_handler = colorlog.StreamHandler(sys.stdout)
    console_handler.setLevel(console_level)

    console_formatter = colorlog.ColoredFormatter(
        "%(log_color)s%(asctime)s - %(levelname)s - %(message)s",
        datefmt='%H:%M:%S',
        log_colors={
            'DEBUG': 'green',
            'INFO': 'cyan',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'red,bg_white'
        }
    )
    console_handler.setFormatter(console_formatter)
    main_logger.addHandler(console_handler)
    return main_logger


logger = setup_logger(__name__)
