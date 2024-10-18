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

@pytest.fixture
def file_storage(tmp_path):
    # Create a FileStorage instance with a temporary directory
    return FileStorage(str(tmp_path))

def test_file_storage_save_text(file_storage, mocker):
    text_data = [{'page_number': 1, 'text': 'Sample text'}]
    
    # Mock open function to test save_text
    mock_open_function = mocker.patch('builtins.open', mock_open())
    
    file_storage.save_text(text_data)
    
    mock_open_function.assert_called_once_with(os.path.join(file_storage.output_directory, 'extracted_text.txt'), 'w')
    mock_open_function().write.assert_called_once_with('Sample text\n')
    logging.info("FileStorage: Text saving test passed.")

def test_file_storage_save_links(file_storage, mocker):
    links_data = [{'url': 'http://example.com', 'page_number': 1}]
    
    # Mock open function to test save_links
    mock_open_function = mocker.patch('builtins.open', mock_open())
    
    file_storage.save_links(links_data)
    
    mock_open_function.assert_called_once_with(os.path.join(file_storage.output_directory, 'extracted_links.txt'), 'w')
    mock_open_function().write.assert_called_once_with('Page 1 -> http://example.com\n')
    logging.info("FileStorage: Links saving test passed.")

def test_file_storage_save_images(file_storage, mocker):
    images_data = [{'image_data': b'\x89PNG...', 'image_extension': 'png', 'page_number': 1}]
    
    # Mock open function to test save_images
    mock_open_function = mocker.patch('builtins.open', mock_open())
    
    file_storage.save_images(images_data)
    
    assert mock_open_function.call_count == 2  # Check that two files are being opened (image and metadata)
    logging.info("FileStorage: Images saving test passed.")

def test_file_storage_save_tables(file_storage, mocker):
    tables_data = [{'table': [['Header1', 'Header2'], ['Row1Col1', 'Row1Col2']], 'page_number': 1}]
    
    # Mock open function to test save_tables
    mock_open_function = mocker.patch('builtins.open', mock_open())
    
    file_storage.save_tables(tables_data)
    
    assert mock_open_function.call_count == 2  # Check that two files are being opened (table and metadata)
    logging.info("FileStorage: Tables saving test passed.")


@pytest.fixture
def mysql_storage(mocker):
    # Mock MySQL connection
    mock_connection = mocker.patch('mysql.connector.connect', return_value=MagicMock())
    storage = MySQLStorage(db_config)
    yield storage
    storage.close()

def test_mysql_storage_save_text(mysql_storage, mocker):
    text_data = [{'page_number': 1, 'text': 'Sample text'}]
    mock_cursor = mysql_storage.cursor
    mock_cursor.execute = MagicMock()
    
    mysql_storage.save_text(text_data)
    
    mock_cursor.execute.assert_called_once_with('''
        INSERT INTO text_data (content, page_number) VALUES (%s, %s)
    ''', ('Sample text', None))
    logging.info("MySQLStorage: Text saving to MySQL test passed.")

def test_mysql_storage_save_images(mysql_storage, mocker):
    images_data = [{'image_data': b'\x89PNG...', 'image_extension': 'png', 'page_number': 1}]
    mock_cursor = mysql_storage.cursor
    mock_cursor.execute = MagicMock()
    
    mysql_storage.save_images(images_data)
    
    mock_cursor.execute.assert_called_once_with('''
        INSERT INTO images_data (image_data, image_extension, page_number) VALUES (%s, %s, %s)
    ''', (b'\x89PNG...', 'png', 1))
    logging.info("MySQLStorage: Images saving to MySQL test passed.")

def test_mysql_storage_save_tables(mysql_storage, mocker):
    tables_data = [{'table': [['Header1', 'Header2'], ['Row1Col1', 'Row1Col2']], 'page_number': 1}]
    mock_cursor = mysql_storage.cursor
    mock_cursor.execute = MagicMock()
    
    mysql_storage.save_tables(tables_data)
    
    mock_cursor.execute.assert_called_once_with('''
        INSERT INTO tables_data (table_data, page_number) VALUES (%s, %s)
    ''', ("[['Header1', 'Header2'], ['Row1Col1', 'Row1Col2']]", None))
    logging.info("MySQLStorage: Tables saving to MySQL test passed.")

def test_mysql_storage_save_links(mysql_storage, mocker):
    links_data = [{'url': 'http://example.com', 'page_number': 1}]
    mock_cursor = mysql_storage.cursor
    mock_cursor.execute = MagicMock()
    
    mysql_storage.save_links(links_data)
    
    mock_cursor.execute.assert_called_once_with('''
        INSERT INTO links_data (url, page_number) VALUES (%s, %s)
    ''', ('http://example.com', None))
    logging.info("MySQLStorage: Links saving to MySQL test passed.")