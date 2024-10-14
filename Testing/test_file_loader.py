# test_file_loader.py

import pytest
from unittest.mock import MagicMock, patch
from src.extractor_file import PDFLoader, DOCXLoader, PPTLoader, DataExtractor, FileStorage  
import logging
from logging_config import setup_logging

# Setup logging for the tests
setup_logging()

@pytest.fixture
def pdf_loader():
    with patch('src.extractor_file.fitz.open') as mock_open:
        mock_open.return_value = MagicMock()
        loader = PDFLoader("test.pdf")
        yield loader

@pytest.fixture
def docx_loader():
    with patch('src.extractor_file.docx.Document') as mock_docx:
        mock_docx.return_value = MagicMock()
        loader = DOCXLoader("test.docx")
        yield loader

@pytest.fixture
def ppt_loader():
    with patch('src.extractor_file.Presentation') as mock_ppt:
        mock_ppt.return_value = MagicMock()
        loader = PPTLoader("test.pptx")
        yield loader

def test_pdf_loader_validation(pdf_loader):
    assert pdf_loader.validate() is True
    pdf_loader.file_path = "invalid_file.txt"
    assert pdf_loader.validate() is False

def test_docx_loader_validation(docx_loader):
    assert docx_loader.validate() is True
    docx_loader.file_path = "invalid_file.txt"
    assert docx_loader.validate() is False

def test_ppt_loader_validation(ppt_loader):
    assert ppt_loader.validate() is True
    ppt_loader.file_path = "invalid_file.txt"
    assert ppt_loader.validate() is False

def test_data_extractor_pdf(pdf_loader):
    extractor = DataExtractor(pdf_loader)
    pdf_loader.doc = MagicMock()
    pdf_loader.doc.load_page.return_value.get_text.return_value = "Sample text"

    text_data = extractor.extract_text()
    assert len(text_data) == 1
    assert text_data[0]['text'] == "Sample text"

def test_data_extractor_docx(docx_loader):
    extractor = DataExtractor(docx_loader)
    docx_loader.doc.paragraphs = [MagicMock(text="Paragraph 1", style=MagicMock(name="style", name="Normal")),
                                   MagicMock(text="Paragraph 2", style=MagicMock(name="style", name="Heading1"))]
    
    text_data = extractor.extract_text()
    assert len(text_data) == 2
    assert text_data[0]['text'] == "Paragraph 1"
    assert text_data[1]['style'] == "Heading1"

def test_data_extractor_ppt(ppt_loader):
    extractor = DataExtractor(ppt_loader)
    ppt_loader.presentation.slides = [MagicMock(shapes=[MagicMock(text="Slide 1 Text"), MagicMock(text="Slide 2 Text")])]
    
    text_data = extractor.extract_text()
    assert len(text_data) == 1
    assert "Slide 1 Text" in text_data[0]['text']

def test_file_storage_save_text():
    storage = FileStorage("test_output")
    storage.save_text(["Test text"])
    with open("test_output/extracted_text.txt", 'r') as f:
        content = f.read().strip()
    assert content == "Test text"

if __name__ == "__main__":
    pytest.main()
