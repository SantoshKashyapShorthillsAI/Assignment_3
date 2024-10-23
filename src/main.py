import os
import shutil  # To delete directories
import json
from dotenv import load_dotenv
from file_loaders import FileLoaderRegistry
from processing import Processing

def main():
    """Main entry point of the application."""
    # Define project root and directories
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    base_dir = os.path.join(project_root, "Documents")
    output_dir = os.path.join(project_root, "Output")

    # Initialize the registry and register loaders for supported file types
    registry = FileLoaderRegistry(output_dir)

    # Uncomment to register additional loaders
    # registry.register_loader('xlsx', XLSXLoader, "XLSX")

    while True:
        # Get the filename from the user
        file_name = input("Enter the filename (with extension): ").strip()
        if file_name.lower() == 'exit':
            print("Exiting the program.")
            break
        file_path = os.path.join(base_dir, file_name)

        # Check if the file exists
        if not os.path.isfile(file_path):
            print(f"The file at the path '{file_path}' does not exist. Please provide a valid relative path.")
            continue  # Prompt for input again if the file does not exist

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

            # Check for missing environment variables
            if None in db_config.values():
                print("Database configuration is missing. Please check your .env file.")
                return

            # Process the file
            try:
                Processing.process_file(loader_class, file_path, output_folder, db_config)
            except Exception as e:
                print(f"An error occurred while processing the file: {e}")
        else:
            print("Unsupported file type. Please enter a valid filename with a supported extension (pdf, docx, pptx, etc.).")
    
if __name__ == "__main__":
    main()
