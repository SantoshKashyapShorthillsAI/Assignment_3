from abc import ABC, abstractmethod
import fitz
import docx
from pptx import Presentation
import os
import csv

class FileLoader(ABC):
    def __init__(self, file_path, expected_extension):
        self.file_path = file_path
        # Store the expected extension in lowercase
        self.expected_extension = expected_extension.lower() 

    def validate_extension(self):
        """Validate the file extension against the expected extension."""
        # Compare the file extension with the expected one, both in lowercase
        if not self.file_path.lower().endswith(self.expected_extension):
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
        """Load the PDF file content.

        Returns:
            fitz.Document: The loaded PDF document.

        Raises:
            ValueError: If the PDF file cannot be opened.
        """
        self.validate_extension()
        try:
            self.doc = fitz.open(self.file_path)
        except Exception as e:
            raise ValueError(f"Failed to load PDF file: {str(e)}")
        return self.doc


class DOCXLoader(FileLoader):
    def __init__(self, file_path):
        super().__init__(file_path, '.docx')
        self.doc = None

    def load(self):
        """Load the DOCX file content.

        Returns:
            docx.Document: The loaded Word document.

        Raises:
            ValueError: If the DOCX file cannot be opened.
        """
        self.validate_extension()
        try:
            self.doc = docx.Document(self.file_path)
        except Exception as e:
            raise ValueError(f"Failed to load DOCX file: {str(e)}")
        return self.doc


class PPTLoader(FileLoader):
    def __init__(self, file_path):
        super().__init__(file_path, '.pptx')
        self.presentation = None

    def load(self):
        """Load the PPTX file content.

        Returns:
            pptx.Presentation: The loaded PowerPoint presentation.

        Raises:
            ValueError: If the PPTX file cannot be opened.
        """
        self.validate_extension()
        try:
            self.presentation = Presentation(self.file_path)
        except Exception as e:
            raise ValueError(f"Failed to load PPTX file: {str(e)}")
        return self.presentation


class FileLoaderRegistry:
    """Registry to map file extensions to loader classes and their output directories."""
    
    def __init__(self, output_dir):
        """Initialize the registry with the base output directory.

        Args:
            output_dir (str): The base directory for output files.
        """
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)  # Ensure base output dir exists
        
        self.loader_map = {
            'pdf': (PDFLoader, os.path.join(self.output_dir, "PDF")),
            'docx': (DOCXLoader, os.path.join(self.output_dir, "DOCX")),
            'pptx': (PPTLoader, os.path.join(self.output_dir, "PPTX")),
        }
        
        # Create subdirectories for loaders
        for _, subdir in self.loader_map.values():
            os.makedirs(subdir, exist_ok=True)

    def register_loader(self, file_extension, loader_class, output_subdir):
        """Register a new file extension with its loader class and output directory."""
        self.loader_map[file_extension] = (loader_class, os.path.join(self.output_dir, output_subdir))

    def get_loader_and_output_dir(self, file_extension):
        """Get the loader class and output directory for the given file extension.

        Args:
            file_extension (str): The file extension to look up.

        Returns:
            tuple: The loader class and corresponding output directory, or None if not found.
        """
        return self.loader_map.get(file_extension)
