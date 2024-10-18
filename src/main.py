"""
main.py

This module serves as the entry point for the application. It facilitates the loading,
processing, and extraction of data from various file types using the registered loaders.
The extracted data is then saved to specified output directories and a MySQL database.
"""

from file_loaders import FileLoaderRegistry
from processing import Processing
import os
import shutil  # To delete directories
from dotenv import load_dotenv
import json


def main():
    """
    Main function to run the file processing application.

    This function performs the following tasks:
    - Defines project root and directories for input and output.
    - Initializes a file loader registry to manage file loaders.
    - Prompts the user for a filename and validates its existence.
    - Extracts the file extension and retrieves the appropriate loader class and output directory.
    - Loads database configuration from environment variables.
    - Processes the file and extracts data using the registered loader.

    Raises:
        FileNotFoundError: If the specified file does not exist.
        ValueError: If the file type is unsupported.
    """
    # Define project root and directories
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    base_dir = os.path.join(project_root, "Documents")
    output_dir = os.path.join(project_root, "Output")

    # Initialize the registry and register loaders for supported file types
    registry = FileLoaderRegistry(output_dir)

    # Uncomment the following line to register XLSX loader (if needed)
    # registry.register_loader('xlsx', XLSXLoader, "XLSX")

    # Get the filename from the user
    file_name = input("Enter the filename (with extension): ").strip()
    file_path = os.path.join(base_dir, file_name)

    # Check if the file exists
    if not os.path.isfile(file_path):
        print(f"The file at the path '{file_path}' does not exist. Please provide a valid relative path.")
    else:
        # Extract file extension and get loader class/output directory from the registry
        file_extension = file_name.split('.')[-1].lower()
        loader_class_output = registry.get_loader_and_output_dir(file_extension)

        if loader_class_output:
            loader_class, output_folder = loader_class_output

            # Get database configuration from environment variables
            load_dotenv()
            db_config = {
                'user': os.getenv('DB_USER'),
                'password': os.getenv('DB_PASSWORD'),
                'host': os.getenv('DB_HOST'),
                'database': os.getenv('DB_DATABASE'),
            }

            # Process the file
            Processing.process_file(loader_class, file_path, output_folder, db_config)
        else:
            print("Unsupported file type. Please enter a valid filename with a supported extension (pdf, docx, pptx, etc.).")


if __name__ == "__main__":
    main()
