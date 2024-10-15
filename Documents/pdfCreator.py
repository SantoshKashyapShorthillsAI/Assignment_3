from fpdf import FPDF

# Create instance of FPDF class
pdf = FPDF()

# Add a page
pdf.add_page()

# Set title
pdf.set_font("Arial", 'B', 16)
pdf.cell(200, 10, txt="Simple PDF with Plain Text", ln=True, align='C')

# Add plain text
pdf.ln(10)  # Line break for spacing
pdf.set_font("Arial", size=12)
pdf.multi_cell(0, 10, txt="This is a simple PDF document created using the FPDF library in Python. "
                           "It contains only plain text without any links, images, or tables. "
                           "You can customize the text as needed.")

# Save the PDF
pdf_file_path = "plain.pdf"
pdf.output(pdf_file_path)

print("Simple PDF created successfully!")
