from fpdf import FPDF

# Create instance of FPDF class
pdf = FPDF()

# Add a page
pdf.add_page()

# Set title
pdf.set_font("Arial", 'B', 16)
pdf.cell(200, 10, txt="PDF with Text, Links, Images, and Tables", ln=True, align='C')

# Add a link
pdf.set_font("Arial", size=12)
pdf.cell(200, 10, txt="Click here to visit Python's official website", ln=True, link="https://www.python.org/")

# Add some text
pdf.ln(10)
pdf.set_font("Arial", size=12)
pdf.multi_cell(0, 10, txt="This is an example of a PDF file that includes text, links, images, and tables using Python and the FPDF library.")

# Add an image
pdf.ln(10)
pdf.image("apple.jpeg", x=50, y=60, w=100)  # Replace 'image_example.png' with your image path

# Add a table
pdf.ln(85)  # Adjust for spacing after the image
pdf.set_font("Arial", size=12)
data = [
    ["ID", "Name", "Age", "City"],
    [1, "John Doe", 28, "New York"],
    [2, "Jane Smith", 34, "London"],
    [3, "Sam Brown", 22, "Sydney"]
]

# Create table header
pdf.cell(40, 10, "ID", 1)
pdf.cell(60, 10, "Name", 1)
pdf.cell(40, 10, "Age", 1)
pdf.cell(50, 10, "City", 1)
pdf.ln()

# Add table rows
for row in data[1:]:
    pdf.cell(40, 10, str(row[0]), 1)
    pdf.cell(60, 10, row[1], 1)
    pdf.cell(40, 10, str(row[2]), 1)
    pdf.cell(50, 10, row[3], 1)
    pdf.ln()

# Save the PDF
pdf.output("example_pdf.pdf")
