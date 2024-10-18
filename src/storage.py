# storage.py
import os
from abc import ABC, abstractmethod
import fitz
import docx
from pptx import Presentation
import csv
import pdfplumber
import mysql.connector

class Storage(ABC):
    """Abstract class for storing extracted data."""

    @abstractmethod
    def save_text(self, text_data):
        """Save extracted text."""
        pass

    @abstractmethod
    def save_images(self, images_data):
        """Save extracted images."""
        pass

    @abstractmethod
    def save_tables(self, tables_data):
        """Save extracted tables."""
        pass

    @abstractmethod
    def save_links(self, links_data):
        """Save extracted links."""
        pass

class FileStorage(Storage):
    """Concrete class for storing extracted data to files."""

    def __init__(self, output_directory):
        """Initialize FileStorage with an output directory."""
        self.output_directory = output_directory
        if not os.path.exists(self.output_directory):
            os.makedirs(self.output_directory)

    def save_text(self, text_data):
        """Save extracted text to a text file."""
        with open(os.path.join(self.output_directory, 'extracted_text.txt'), 'w') as f:
            for entry in text_data:
                f.write(f"{entry}\n")

    def save_links(self, links_data):
        """Save extracted hyperlinks with page/slide/paragraph number to a text file."""
        with open(os.path.join(self.output_directory, 'extracted_links.txt'), 'w') as f:
            for link in links_data:
                # Determine whether it's a PDF page, PowerPoint slide, or Word paragraph
                location = ""
                if 'page_number' in link:
                    location = f"Page {link['page_number']}"  # For PDF
                elif 'slide_number' in link:
                    location = f"Slide {link['slide_number']}"  # For PowerPoint
                elif 'paragraph_number' in link:
                    location = f"Paragraph {link['paragraph_number']}"  # For Word

                # Use .get() to avoid KeyError if 'url' is missing
                url = link.get('url', 'No URL')  # Default to 'No URL' if 'url' key is missing

                # Write the location (page/slide/paragraph) and URL to the file
                f.write(f"{location} -> {url}\n")



    def save_images(self, images_data):
        """Save extracted images and metadata to the output directory."""
        for i, image in enumerate(images_data):
            image_extension = image.get("image_extension", "png")  # Default to PNG if not provided
            image_path = os.path.join(self.output_directory, f'image_{i}.{image_extension}')
            metadata_path = os.path.join(self.output_directory, f'image_{i}_metadata.txt')

            # Save the image file
            with open(image_path, 'wb') as img_file:
                img_file.write(image['image_data'])

            # Create and save the image metadata
            with open(metadata_path, 'w') as metafile:
                metafile.write(f"Image {i + 1} Metadata\n")
                if 'page_number' in image:
                    metafile.write(f"Extracted from PDF - Page {image['page_number']}\n")
                elif 'slide_number' in image:
                    metafile.write(f"Extracted from PowerPoint - Slide {image['slide_number']}\n")
                else:
                    metafile.write("Extracted from Word document\n")
                
                metafile.write(f"Image Extension: {image_extension}\n")
                metafile.write(f"Image Size: {len(image['image_data'])} bytes\n")




    def save_tables(self, tables_data):
        """Save extracted tables as CSV files along with metadata."""
        for i, table in enumerate(tables_data):
            # Safely get 'page_number', 'slide_number', or use 'unknown' if missing
            page_number = table.get("page_number", table.get("slide_number", "unknown_location"))
            
            # Safely get table data
            table_rows = table.get("table", [])

            # Define paths for the CSV file and metadata file
            table_path = os.path.join(self.output_directory, f'table_{i}_location_{page_number}.csv')
            metadata_path = os.path.join(self.output_directory, f'table_{i}_location_{page_number}_metadata.txt')

            # Save the table data as a CSV file
            with open(table_path, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerows(table_rows)

            # Save metadata as a separate .txt file
            with open(metadata_path, 'w') as metafile:
                metafile.write(f"Table {i + 1} Metadata\n")
                if 'page_number' in table:
                    metafile.write(f"Extracted from PDF - Page {table['page_number']}\n")
                elif 'slide_number' in table:
                    metafile.write(f"Extracted from PowerPoint - Slide {table['slide_number']}\n")
                else:
                    metafile.write("Extracted from Word document\n")

                # You can add more metadata if needed (e.g., source, timestamp, etc.)
                metafile.write(f"Number of rows: {len(table_rows)}\n")
                if table_rows:
                    metafile.write(f"Number of columns: {len(table_rows[0])}\n")
                else:
                    metafile.write("Number of columns: 0\n")

class MySQLStorage(Storage):
    def __init__(self, db_config):
        self.connection = mysql.connector.connect(**db_config)
        self.cursor = self.connection.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS text_data (
                id INT AUTO_INCREMENT PRIMARY KEY,
                content TEXT NOT NULL,
                page_number INT
            )
        ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS images_data (
                id INT AUTO_INCREMENT PRIMARY KEY,
                image_data LONGBLOB NOT NULL,
                image_extension VARCHAR(10),
                page_number INT
            )
        ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS tables_data (
                id INT AUTO_INCREMENT PRIMARY KEY,
                table_data TEXT NOT NULL,
                page_number INT
            )
        ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS links_data (
                id INT AUTO_INCREMENT PRIMARY KEY,
                url TEXT NOT NULL,
                page_number INT
            )
        ''')
        self.connection.commit()

    def save_text(self, text_data):
        for item in text_data:
            self.cursor.execute('''
                INSERT INTO text_data (content, page_number) VALUES (%s, %s)
            ''', (item.get("text", ""), item.get("slide_number", None))) 
        self.connection.commit()


    def save_images(self, images_data):
        for item in images_data:
            self.cursor.execute('''
                INSERT INTO images_data (image_data, image_extension, page_number) VALUES (%s, %s, %s)
            ''', (item["image_data"], item["image_extension"], item.get("page_number", None)))
        self.connection.commit()

    def save_tables(self, tables_data):
        for item in tables_data:
            self.cursor.execute('''
                INSERT INTO tables_data (table_data, page_number) VALUES (%s, %s)
            ''', (str(item["table"]), item.get("page_number", None)))
        self.connection.commit()

    def save_links(self, links_data):
        for item in links_data:
            url = item.get("url")
            if url:  # Ensure url is not None or empty
                self.cursor.execute('''
                    INSERT INTO links_data (url, page_number) VALUES (%s, %s)
                ''', (url, item.get("page_number", None)))
        self.connection.commit()

    def close(self):
        self.cursor.close()
        self.connection.close()                
