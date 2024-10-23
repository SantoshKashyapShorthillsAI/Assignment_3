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
from unittest.mock import MagicMock
import pytest
from data_extractor import DataExtractor

@pytest.fixture
def mock_pdf_loader():
    loader = MagicMock()
    loader.__class__ = PDFLoader  # Simulate that this is a PDFLoader
    loader.doc = MagicMock()  # Mock the 'doc' attribute
    loader.doc.load_page = MagicMock(return_value=MagicMock(get_text=MagicMock(return_value="Sample text")))  # Mock PDF page text extraction
    return loader

@pytest.fixture
def mock_docx_loader():
    loader = MagicMock()
    loader.__class__ = DOCXLoader  # Simulate that this is a DOCXLoader
    loader.doc = MagicMock()  # Mock the 'doc' attribute
    loader.doc.paragraphs = [MagicMock(text="Sample text", style=MagicMock(name="Normal"))]  # Mock DOCX paragraphs
    return loader

@pytest.fixture
def mock_ppt_loader():
    loader = MagicMock()
    loader.__class__ = PPTLoader  # Simulate that this is a PPTLoader
    loader.presentation = MagicMock()  # Mock the 'presentation' attribute
    slide_mock = MagicMock()
    slide_mock.shapes = [MagicMock(text="Sample slide text")]  # Mock slide shapes and text
    loader.presentation.slides = [slide_mock]  # Mock PPTX slides
    return loader

def test_extract_pdf_text(mock_pdf_loader):
    """Test extracting text from a PDF."""
    extractor = DataExtractor(mock_pdf_loader)
    result = extractor.extract_text()
    assert result == [{"page_number": 1, "text": "Sample text"}]

def test_extract_docx_text(mock_docx_loader):
    """Test extracting text from a DOCX."""
    extractor = DataExtractor(mock_docx_loader)
    result = extractor.extract_text()
    assert result == [{"text": "Sample text", "style": "Normal"}]

def test_extract_ppt_text(mock_ppt_loader):
    """Test extracting text from a PPTX."""
    extractor = DataExtractor(mock_ppt_loader)
    result = extractor.extract_text()
    assert result == [{"slide_number": 1, "text": "Sample slide text"}]
