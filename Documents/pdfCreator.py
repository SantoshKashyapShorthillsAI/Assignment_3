from fpdf import FPDF

class PDF(FPDF):
    def header(self):
        # Custom header
        self.set_font("Arial", 'B', 12)
        self.cell(0, 10, 'Multi-Column PDF Example', 0, 1, 'C')

    def footer(self):
        # Custom footer
        self.set_y(-15)
        self.set_font("Arial", 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

    def multi_column(self, texts, col_count=2):
        # Define column width
        col_width = self.w / col_count
        # Loop through the texts and add them to the PDF
        for text in texts:
            # Start new cell for each column
            self.cell(col_width, 10, txt=text, border=1, ln=3, align='L')

# Create instance of PDF class
pdf = PDF()

# Add a page
pdf.add_page()

# Set font
pdf.set_font("Arial", size=12)

# Sample dummy text data for multiple columns
dummy_text = (
    "Lorem ipsum dolor sit amet, consectetur adipiscing elit. "
    "Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. "
    "Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. "
    "Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. "
    "Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."
)

# Create a list with repeated dummy text to fill multiple columns
text_data = [dummy_text] * 10  # Duplicate the dummy text for 10 entries

# Add multi-column text
pdf.multi_column(text_data, col_count=2)

# Save the PDF
pdf_file_path = "multi_column.pdf"
pdf.output(pdf_file_path)

print("Multi-column PDF with dummy text created successfully!")
