from abc import ABC, abstractmethod
import fitz
import docx
from pptx import Presentation
import os
import csv

class FileLoader(ABC):
    def __init__(self, file_path, expected_extension):
        self.file_path = file_path
        self.expected_extension = expected_extension

    def validate_extension(self):
        if not self.file_path.endswith(self.expected_extension):
            raise ValueError(f"Invalid file format. Expected {self.expected_extension}.")

    @abstractmethod
    def load(self):
        """Load the file content."""
        pass


class PDFLoader(FileLoader):
    def __init__(self, file_path):
        super().__init__(file_path, '.pdf')
        self.doc = None

    def load(self):
        self.validate_extension()
        self.doc = fitz.open(self.file_path)
        return self.doc


class DOCXLoader(FileLoader):
    def __init__(self, file_path):
        super().__init__(file_path, '.docx')
        self.doc = None

    def load(self):
        self.validate_extension()
        self.doc = docx.Document(self.file_path)
        return self.doc


class PPTLoader(FileLoader):
    def __init__(self, file_path):
        super().__init__(file_path, '.pptx')
        self.presentation = None

    def load(self):
        self.validate_extension()
        self.presentation = Presentation(self.file_path)
        return self.presentation


class FileLoaderRegistry:
    """Registry to map file extensions to loader classes and their output directories."""
    
    def __init__(self, output_dir):
        self.output_dir = output_dir
        self.loader_map = {
            'pdf': (PDFLoader, os.path.join(self.output_dir, "PDF")),
            'docx': (DOCXLoader, os.path.join(self.output_dir, "DOCX")),
            'pptx': (PPTLoader, os.path.join(self.output_dir, "PPTX")),
        }

    def register_loader(self, file_extension, loader_class, output_subdir):
        """Register a new file extension with its loader class and output directory."""
        self.loader_map[file_extension] = (loader_class, os.path.join(self.output_dir, output_subdir))

    def get_loader_and_output_dir(self, file_extension):
        """Get the loader class and output directory for the given file extension."""
        return self.loader_map.get(file_extension)
