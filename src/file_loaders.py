from abc import ABC, abstractmethod
import fitz
import docx
from pptx import Presentation
import os
import csv

class FileLoader(ABC):
    """
    Abstract base class for loading files.

    Attributes:
        file_path (str): Path to the file to be loaded.
        expected_extension (str): Expected file extension.

    Methods:
        validate_extension(): Validates that the file has the expected extension.
        load(): Abstract method for loading the file content.
    """

    def __init__(self, file_path, expected_extension):
        """
        Initializes the FileLoader.

        Args:
            file_path (str): Path to the file.
            expected_extension (str): Expected file extension for validation.
        """
        self.file_path = file_path
        self.expected_extension = expected_extension

    def validate_extension(self):
        """Validates the file extension against the expected extension."""
        if not self.file_path.endswith(self.expected_extension):
            raise ValueError(f"Invalid file format. Expected {self.expected_extension}.")

    @abstractmethod
    def load(self):
        """Load the file content. To be implemented by subclasses."""
        pass


class PDFLoader(FileLoader):
    """
    Loader for PDF files.

    Inherits from FileLoader.

    Methods:
        load(): Loads the PDF file and returns the document object.
    """

    def __init__(self, file_path):
        """
        Initializes the PDFLoader.

        Args:
            file_path (str): Path to the PDF file.
        """
        super().__init__(file_path, '.pdf')
        self.doc = None

    def load(self):
        """Loads the PDF file and returns the document object."""
        try:
            self.validate_extension()
            self.doc = fitz.open(self.file_path)
            return self.doc
        except ValueError as e:
            print(f"Error in validation: {e}")
            return None
        except Exception as e:
            print(f"Failed to load PDF file: {e}")
            return None


class DOCXLoader(FileLoader):
    """
    Loader for DOCX files.

    Inherits from FileLoader.

    Methods:
        load(): Loads the DOCX file and returns the document object.
    """

    def __init__(self, file_path):
        """
        Initializes the DOCXLoader.

        Args:
            file_path (str): Path to the DOCX file.
        """
        super().__init__(file_path, '.docx')
        self.doc = None

    def load(self):
        """Loads the DOCX file and returns the document object."""
        try:
            self.validate_extension()
            self.doc = docx.Document(self.file_path)
            return self.doc
        except ValueError as e:
            print(f"Error in validation: {e}")
            return None
        except Exception as e:
            print(f"Failed to load DOCX file: {e}")
            return None


class PPTLoader(FileLoader):
    """
    Loader for PPTX files.

    Inherits from FileLoader.

    Methods:
        load(): Loads the PPTX file and returns the presentation object.
    """

    def __init__(self, file_path):
        """
        Initializes the PPTLoader.

        Args:
            file_path (str): Path to the PPTX file.
        """
        super().__init__(file_path, '.pptx')
        self.presentation = None

    def load(self):
        """Loads the PPTX file and returns the presentation object."""
        try:
            self.validate_extension()
            self.presentation = Presentation(self.file_path)
            return self.presentation
        except ValueError as e:
            print(f"Error in validation: {e}")
            return None
        except Exception as e:
            print(f"Failed to load PPTX file: {e}")
            return None


class FileLoaderRegistry:
    """
    Registry to manage file loaders and their associated output directories.

    Attributes:
        output_dir (str): Directory where output files are saved.
        loader_map (dict): Mapping of file extensions to their respective loader classes and output directories.

    Methods:
        register_loader(file_extension, loader_class, output_subdir):
            Registers a new file extension with its loader class and output directory.
        
        get_loader_and_output_dir(file_extension):
            Retrieves the loader class and output directory for a given file extension.
    """

    def __init__(self, output_dir):
        """
        Initializes the FileLoaderRegistry.

        Args:
            output_dir (str): Base output directory for loaded files.
        """
        self.output_dir = output_dir
        self.loader_map = {
            'pdf': (PDFLoader, os.path.join(self.output_dir, "PDF")),
            'docx': (DOCXLoader, os.path.join(self.output_dir, "DOCX")),
            'pptx': (PPTLoader, os.path.join(self.output_dir, "PPTX")),
        }

    def register_loader(self, file_extension, loader_class, output_subdir):
        """
        Registers a new file extension with its loader class and output directory.

        Args:
            file_extension (str): The file extension to register.
            loader_class (type): The loader class for the file type.
            output_subdir (str): Subdirectory where loaded files will be saved.
        """
        self.loader_map[file_extension] = (loader_class, os.path.join(self.output_dir, output_subdir))

    def get_loader_and_output_dir(self, file_extension):
        """
        Retrieves the loader class and output directory for the given file extension.

        Args:
            file_extension (str): The file extension for which to get the loader.

        Returns:
            tuple: A tuple containing the loader class and the associated output directory,
            or None if the file extension is not registered.
        """
        return self.loader_map.get(file_extension)

