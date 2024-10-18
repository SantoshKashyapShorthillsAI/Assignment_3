"""
processing.py

This module handles the processing of files to extract data (text, links, images, tables)
using the DataExtractor class. It supports saving the extracted data to both file storage
and MySQL database storage.
"""

from data_extractor import DataExtractor
from storage import FileStorage, MySQLStorage
import os
import shutil  # To delete directories


class Processing:
    """Class responsible for processing files and managing data extraction and storage."""

    @staticmethod
    def process_file(loader_class, file_path, output_folder, db_config):
        """
        Process a file to extract data and save it to specified storage.

        This method deletes any existing output folder for the file type, creates a new one,
        extracts data using the DataExtractor, and saves the data to both file storage
        and MySQL database.

        Args:
            loader_class (class): The loader class to handle the specific file type.
            file_path (str): The path to the file to be processed.
            output_folder (str): The folder where extracted data will be saved.
            db_config (dict): Configuration dictionary for MySQL database connection.

        Raises:
            Exception: Raises an exception if the data extraction fails or any storage operation fails.
        """
        # Delete the existing output folder for the file type and recreate it
        if os.path.exists(output_folder):
            shutil.rmtree(output_folder)
        os.makedirs(output_folder, exist_ok=True)

        # Initialize the loader and extractor
        loader = loader_class(file_path)
        extractor = DataExtractor(loader)

        # Extract data
        text_data = extractor.extract_text()
        link_data = extractor.extract_links()
        images_data = extractor.extract_images()
        tables_data = extractor.extract_tables()

        # Save data to file storage
        file_storage = FileStorage(output_folder)
        file_storage.save_text(text_data)
        file_storage.save_links(link_data)
        file_storage.save_images(images_data)
        file_storage.save_tables(tables_data)

        # Save data to MySQL storage
        mysql_storage = MySQLStorage(db_config)
        mysql_storage.save_text(text_data)
        mysql_storage.save_images(images_data)
        mysql_storage.save_tables(tables_data)
        mysql_storage.save_links(link_data)
        mysql_storage.close()
