# Assignment_3
Assignment 3 : Python

## Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/SantoshKashyapShorthillsAI/Assignment_3.git
   cd Assignment_3
   ```

2. **Install the required dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

3. **Set up MySQL database**:

   Create a MySQL database and configure the connection details in the script.

   ```sql
   CREATE DATABASE sql_storage;
   ```

   Update the `db_config` in the script with your MySQL credentials:

   ```python
   db_config = {
       'user': 'your_username',
       'password': 'your_password',
       'host': 'localhost',
       'database': 'sql_storage',
   }
   ```

---

## Usage 

1. **Run the script**:

   To process a document, navigate to the project directory and run the following command:

   ```bash
   cd src
   python3 main.py
   ```

   Prompted to enter the filename (with extension) of the document to process. Ensure the file is located in the appropriate directory i.e Documents.

2. **Supported file types**: It supports `PDF`, `DOCX`, and `PPTX` files. Once processed, the extracted data will be saved both locally and in the MySQL database.

---

## Supported File Formats

- **PDF** (`.pdf`): Extracts text, links, images, and tables.
- **DOCX** (`.docx`): Extracts text, links, images, and tables.
- **PPTX** (`.pptx`): Extracts text, links, images, and tables.
