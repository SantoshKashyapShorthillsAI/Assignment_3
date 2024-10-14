# logging_config.py

import logging

def setup_logging():
    logging.basicConfig(
        filename='test_log.log',
        level=logging.DEBUG,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
