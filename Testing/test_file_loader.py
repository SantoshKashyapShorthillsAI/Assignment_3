import pytest
import os
import logging
from unittest.mock import MagicMock
from datetime import datetime
import sys

# Import mocker from pytest-mock if needed
from pytest_mock import mocker 

# Append the src directory to the system path if not already done
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from file_loaders import PDFLoader, DOCXLoader, PPTLoader

# Sample file paths
pdf_path = '/home/shtlp_0103/Assignment_3/Documents/sample.pdf'
docx_path = '/home/shtlp_0103/Assignment_3/Documents/sample.docx'
pptx_path = '/home/shtlp_0103/Assignment_3/Documents/sample.pptx'
output_folder = '/home/shtlp_0103/Assignment_3/Testing/log_dir'

# Set up logging to file and console
log_filename = os.path.join(output_folder, f'test_results_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log')
file_handler = logging.FileHandler(log_filename, 'w')
console_handler = logging.StreamHandler()

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
logger.addHandler(file_handler)
logger.addHandler(console_handler)

def test_logging():
    logging.info("Test case for logging.")
    assert True

# PDFLoader Tests
def test_pdf_loader_valid_file():
    pdf_loader = PDFLoader(pdf_path)
    try:
        pdf_loader.validate_extension()
        logging.info("PDFLoader: Valid PDF file test passed.")
    except ValueError:
        pytest.fail("PDFLoader: File validation failed for a valid PDF file.")

def test_pdf_loader_invalid_file():
    pdf_loader = PDFLoader('invalid.txt')
    with pytest.raises(ValueError):
        pdf_loader.validate_extension()
    logging.info("PDFLoader: Invalid file format test passed.")

def test_pdf_loader_load_method(mocker):
    pdf_loader = PDFLoader(pdf_path)
    mock_open = mocker.patch('fitz.open', return_value=MagicMock())
    assert pdf_loader.load() is not None, "PDFLoader: Failed to load a valid PDF."
    logging.info("PDFLoader: PDF loading test passed.")
    mock_open.assert_called_once_with(pdf_path)

# DOCXLoader Tests
def test_docx_loader_valid_file():
    docx_loader = DOCXLoader(docx_path)
    try:
        docx_loader.validate_extension()
        logging.info("DOCXLoader: Valid DOCX file test passed.")
    except ValueError:
        pytest.fail("DOCXLoader: File validation failed for a valid DOCX file.")

def test_docx_loader_load_method(mocker):
    docx_loader = DOCXLoader(docx_path)
    mock_open = mocker.patch('docx.Document', return_value=MagicMock())
    assert docx_loader.load() is not None, "DOCXLoader: Failed to load a valid DOCX."
    logging.info("DOCXLoader: DOCX loading test passed.")
    mock_open.assert_called_once_with(docx_path)

# PPTLoader Tests
def test_ppt_loader_valid_file():
    ppt_loader = PPTLoader(pptx_path)
    try:
        ppt_loader.validate_extension()
        logging.info("PPTLoader: Valid PPTX file test passed.")
    except ValueError:
        pytest.fail("PPTLoader: File validation failed for a valid PPTX file.")

def test_ppt_loader_load_method(mocker):
    ppt_loader = PPTLoader(pptx_path)
    mock_open = mocker.patch('pptx.Presentation', return_value=MagicMock())
    assert ppt_loader.load() is not None, "PPTLoader: Failed to load a valid PPTX."
    logging.info("PPTLoader: PPTX loading test passed.")
    mock_open.assert_called_once_with(pptx_path)
