# processing.py
from data_extractor import DataExtractor
from storage import FileStorage , MySQLStorage
import os
import shutil  # To delete directories



class Processing:
    @staticmethod
    def process_file(loader_class, file_path, output_folder, db_config):
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


