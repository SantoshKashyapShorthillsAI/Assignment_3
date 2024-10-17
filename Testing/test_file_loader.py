import pytest
import os
import logging
from unittest.mock import MagicMock

import sys
sys.path.append("/home/shtlp_0103/Assignment_3")
from src.extractor import PDFLoader, DOCXLoader, PPTLoader, DataExtractor, FileStorage, MySQLStorage


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

def test_logging():
    logging.info("Test case for logging.")
    assert True

# Test cases for the PDFLoader class
def test_pdf_loader_valid_file():
    pdf_loader = PDFLoader(pdf_path)
    assert pdf_loader.validate(), "PDFLoader: File validation failed for a valid PDF file."
    logging.info("PDFLoader: Valid PDF file test passed.")
    

def test_pdf_loader_invalid_file():
    pdf_loader = PDFLoader('invalid.txt')
    assert not pdf_loader.validate(), "PDFLoader: File validation should fail for non-PDF files."
    logging.info("PDFLoader: Invalid file format test passed.")

def test_pdf_loader_load_method(mocker):
    pdf_loader = PDFLoader(pdf_path)
    mock_open = mocker.patch('fitz.open', return_value=MagicMock())
    assert pdf_loader.load(), "PDFLoader: Failed to load a valid PDF."
    logging.info("PDFLoader: PDF loading test passed.")
    mock_open.assert_called_once_with(pdf_path)

# # Test cases for DOCXLoader class
def test_docx_loader_valid_file():
    docx_loader = DOCXLoader(docx_path)
    assert docx_loader.validate(), "DOCXLoader: File validation failed for a valid DOCX file."
    logging.info("DOCXLoader: Valid DOCX file test passed.")

def test_docx_loader_load_method(mocker):
    docx_loader = DOCXLoader(docx_path)
    mock_open = mocker.patch('docx.Document', return_value=MagicMock())
    assert docx_loader.load(), "DOCXLoader: Failed to load a valid DOCX."
    logging.info("DOCXLoader: DOCX loading test passed.")
    mock_open.assert_called_once_with(docx_path)

# # Test cases for PPTLoader class
def test_ppt_loader_valid_file():
    ppt_loader = PPTLoader(pptx_path)
    assert ppt_loader.validate(), "PPTLoader: File validation failed for a valid PPTX file."
    logging.info("PPTLoader: Valid PPTX file test passed.")


def test_ppt_loader_load_method(mocker):
    ppt_loader = PPTLoader(pptx_path)
    mock_open = mocker.patch('pptx.Presentation', return_value=MagicMock())
    
    assert ppt_loader.load() is not None, "PPTLoader: Failed to load a valid PPTX."
    logging.info("PPTLoader: PPTX loading test passed.")
    
    # Check that the Presentation was called with the correct file path
    mock_open.assert_called_once_with(pptx_path)
