from fpdf import FPDF

class PDF(FPDF):
    def header(self):
        self.set_font("Arial", 'B', 14)
        self.cell(0, 10, 'PDF with Annotations Example', 0, 1, 'C')

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

    def add_link_annotation(self, x, y, width, height, url):
        # Add a clickable annotation link to the PDF
        self.link(x, y, width, height, url)

    def add_text_annotation(self, x, y, width, height, text):
        # Draw a border for the annotation
        self.set_xy(x, y)
        self.set_draw_color(255, 0, 0)  # Red border for the text annotation
        self.cell(width, height, border=1)

        # Add the annotation text as a tooltip-like comment
        self.set_xy(x + 1, y + 1)  # Move inside the border
        self.set_font("Arial", '', 12)
        self.multi_cell(width - 2, 10, text)  # Adjust to fit within the box


# Create an instance of the PDF class
pdf = PDF()

# Add a page
pdf.add_page()

# Set font for main content
pdf.set_font("Arial", size=12)

# Add some text
pdf.cell(0, 10, "This is a PDF with annotations (links and text boxes).", ln=True)

# Add a clickable link annotation
pdf.set_xy(10, 30)
pdf.set_font("Arial", 'U', 12)
pdf.set_text_color(0, 0, 255)  # Blue color for link
pdf.cell(0, 10, 'Visit OpenAI website', ln=True)
pdf.add_link_annotation(10, 30, 80, 10, "https://www.openai.com")

# Add a text box annotation
pdf.set_xy(10, 50)
pdf.add_text_annotation(10, 50, 80, 20, "This is a text annotation inside a box. It can be used to comment on specific areas.")

# Save the PDF
pdf_file_path = "annotations.pdf"
pdf.output(pdf_file_path)

print("PDF with annotations created successfully!")
