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


# Mock data for different file types
mock_pdf_text = [
    {"page_number": 1, "text": "Sample PDF text."},
    {"page_number": 2, "text": "Another page of PDF text."}
]

mock_pdf_links = [
    {"page_number": 1, "url": "http://example.com"},
    {"page_number": 2, "url": "http://example.org"}
]

mock_pdf_images = [
    {"page_number": 1, "image_data": b'fake_image_data', "image_extension": "png"}
]

mock_pdf_tables = [
    {"page_number": 1, "table": [["Header1", "Header2"], ["Row1Col1", "Row1Col2"]]}
]

mock_docx_text = [
    {"text": "Sample DOCX text.", "style": "Normal"},
]

mock_docx_links = [
    {"url": "http://example.com", "style": "Hyperlink"}
]

mock_docx_images = [
    {"image_data": b'fake_image_data', "image_extension": "jpeg"}
]

mock_docx_tables = [
    {"table": [["Header1", "Header2"], ["Row1Col1", "Row1Col2"]]}
]

mock_ppt_text = [
    {"slide_number": 1, "text": "Sample PPT text."}
]

mock_ppt_links = [
    {"slide_number": 1, "url": "http://example.com"}
]

mock_ppt_images = [
    {"slide_number": 1, "image_data": b'fake_image_data', "image_extension": "bmp"}
]

mock_ppt_tables = [
    {"slide_number": 1, "table": [["Header1", "Header2"], ["Row1Col1", "Row1Col2"]]}
]

@pytest.fixture
def pdf_loader_mock():
    mock_loader = PDFLoader("dummy.pdf")
    mock_loader.doc = MagicMock()
    mock_loader.doc.load_page.return_value.get_text.return_value = "Sample PDF text."
    mock_loader.doc.get_links.return_value = [{'uri': 'http://example.com'}]
    mock_loader.doc.get_images.return_value = [(1, 0, 0)]
    mock_loader.doc.extract_image.return_value = {"image": b'fake_image_data', "ext": "png"}
    return mock_loader

@pytest.fixture
def docx_loader_mock():
    mock_loader = DOCXLoader("dummy.docx")
    mock_loader.doc = MagicMock()
    mock_loader.doc.paragraphs = [MagicMock(text="Sample DOCX text.", style=MagicMock(name='Normal'))]
    mock_loader.doc.part.rels.values.return_value = [MagicMock(target_ref="http://example.com")]
    return mock_loader

@pytest.fixture
def ppt_loader_mock():
    mock_loader = PPTLoader("dummy.pptx")
    mock_loader.presentation = MagicMock()
    slide_mock = MagicMock()
    slide_mock.shapes = [MagicMock(text="Sample PPT text.")]
    mock_loader.presentation.slides = [slide_mock]
    return mock_loader

def test_extract_text_pdf(pdf_loader_mock):
    extractor = DataExtractor(pdf_loader_mock)
    text_data = extractor.extract_text()
    assert len(text_data) == 2  # Expecting two pages of text
    assert text_data[0]["text"] == "Sample PDF text."

def test_extract_links_pdf(pdf_loader_mock):
    extractor = DataExtractor(pdf_loader_mock)
    link_data = extractor.extract_links()
    assert len(link_data) == 1  # Expecting one link
    assert link_data[0]["url"] == "http://example.com"

def test_extract_images_pdf(pdf_loader_mock):
    extractor = DataExtractor(pdf_loader_mock)
    images_data = extractor.extract_images()
    assert len(images_data) == 1  # Expecting one image
    assert images_data[0]["image_extension"] == "png"

# def test_extract_tables_pdf(pdf_loader_mock):
#     extractor = DataExtractor(pdf_loader_mock)
#     tables_data = extractor.extract_tables()
#     assert len(tables_data) == 1  # Expecting one table
#     assert tables_data[0]["table"] == [["Header1", "Header2"], ["Row1Col1", "Row1Col2"]]

# def test_extract_text_docx(docx_loader_mock):
#     extractor = DataExtractor(docx_loader_mock)
#     text_data = extractor.extract_text()
#     assert len(text_data) == 1
#     assert text_data[0]["text"] == "Sample DOCX text."

# def test_extract_links_docx(docx_loader_mock):
#     extractor = DataExtractor(docx_loader_mock)
#     link_data = extractor.extract_links()
#     assert len(link_data) == 1
#     assert link_data[0]["url"] == "http://example.com"

# def test_extract_images_docx(docx_loader_mock):
#     extractor = DataExtractor(docx_loader_mock)
#     images_data = extractor.extract_images()
#     assert len(images_data) == 1
#     assert images_data[0]["image_extension"] == "jpeg"

# def test_extract_tables_docx(docx_loader_mock):
#     extractor = DataExtractor(docx_loader_mock)
#     tables_data = extractor.extract_tables()
#     assert len(tables_data) == 1
#     assert tables_data[0]["table"] == [["Header1", "Header2"], ["Row1Col1", "Row1Col2"]]

# def test_extract_text_ppt(ppt_loader_mock):
#     extractor = DataExtractor(ppt_loader_mock)
#     text_data = extractor.extract_text()
#     assert len(text_data) == 1
#     assert text_data[0]["text"] == "Sample PPT text."

# def test_extract_links_ppt(ppt_loader_mock):
#     extractor = DataExtractor(ppt_loader_mock)
#     link_data = extractor.extract_links()
#     assert len(link_data) == 1
#     assert link_data[0]["url"] == "http://example.com"

# def test_extract_images_ppt(ppt_loader_mock):
#     extractor = DataExtractor(ppt_loader_mock)
#     images_data = extractor.extract_images()
#     assert len(images_data) == 1
#     assert images_data[0]["image_extension"] == "bmp"

# def test_extract_tables_ppt(ppt_loader_mock):
#     extractor = DataExtractor(ppt_loader_mock)
#     tables_data = extractor.extract_tables()
#     assert len(tables_data) == 1
#     assert tables_data[0]["table"] == [["Header1", "Header2"], ["Row1Col1", "Row1Col2"]]

# # Test cases for DataExtractor class
# def test_extract_text_pdf(mocker):
#     pdf_loader = PDFLoader(pdf_path)
#     mocker.patch('fitz.open', return_value=MagicMock())
#     extractor = DataExtractor(pdf_loader)
#     mock_extract = mocker.patch.object(extractor, '_extract_pdf_text', return_value=[{'page_number': 1, 'text': 'Sample text'}])
#     text = extractor.extract_text()
#     assert text == [{'page_number': 1, 'text': 'Sample text'}], "DataExtractor: Text extraction failed."
#     logging.info("DataExtractor: PDF text extraction test passed.")
#     mock_extract.assert_called_once()