import pytest
import os
import logging
from unittest.mock import MagicMock
import sys
import os

# Append the src directory to the system path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from file_loaders import PDFLoader, DOCXLoader, PPTLoader

from data_extractor import DataExtractor
from storage import FileStorage, MySQLStorage

# Sample PDF, DOCX, and PPTX paths
pdf_path = '/home/shtlp_0103/Assignment_3/Documents/sample.pdf'
docx_path = '/home/shtlp_0103/Assignment_3/Documents/sample.docx'
pptx_path = '/home/shtlp_0103/Assignment_3/Documents/sample.pptx'
output_folder = '/home/shtlp_0103/Assignment_3/Output'

# Mock the database configuration for MySQLStorage
db_config = {
                'user': os.getenv('DB_USER'),
                'password': os.getenv('DB_PASSWORD'),
                'host': os.getenv('DB_HOST'),
                'database': 'test_db',
            }

# Set up logging to file and console
logger = logging.getLogger()
logger.setLevel(logging.INFO)

from datetime import datetime
log_filename = f'test_results_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'
file_handler = logging.FileHandler(log_filename, 'w')

console_handler = logging.StreamHandler()

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(console_handler)
logger.setLevel(logging.DEBUG)

# Test cases for FileStorage class
def test_file_storage_save_text(mocker):
    file_storage = FileStorage(output_folder)
    mock_open = mocker.patch('builtins.open', mocker.mock_open())
    text_data = [{'page_number': 1, 'text': 'Sample text'}]
    file_storage.save_text(text_data)
    mock_open.assert_called_once_with(os.path.join(output_folder, 'extracted_text.txt'), 'w')
    logging.info("FileStorage: Text saving test passed.")

# Test cases for MySQLStorage class (mocking database connection)
def test_mysql_storage_save_text(mocker):
    mock_connection = mocker.patch('mysql.connector.connect', return_value=MagicMock())
    mysql_storage = MySQLStorage(db_config)
    text_data = [{'page_number': 1, 'text': 'Sample text'}]
    mysql_storage.save_text(text_data)
    mock_connection.assert_called_once()
    logging.info("MySQLStorage: Text saving to MySQL test passed.")
