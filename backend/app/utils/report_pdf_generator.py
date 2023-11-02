from fpdf import FPDF
from io import BytesIO
from datetime import datetime

# from .document_retriever import upload_document_to_s3


class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'Report', 0, 1, 'C')

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, 'Page ' + str(self.page_no()), 0, 0, 'C')

    def create_report(self, data):
        self.add_page()
        self.set_font('Arial', '', 12)
        for key, value in data.items():
            self.cell(0, 10, f'{key}: {value}', 0, 1, 'L')


def create_pdf(data):
    pdf = PDF()
    pdf.create_report(data)
    
    # Use a BytesIO buffer to hold the PDF in-memory
    pdf_buffer = BytesIO()
    
    # Get the content of the PDF as a string
    pdf_content = pdf.output(dest='S')
    
    # Write the content to the buffer
    pdf_buffer.write(pdf_content.encode('latin-1'))
    
    # Reset buffer position to beginning
    pdf_buffer.seek(0)
    # Generate a filename (could be based on the content or any other logic you prefer)
    file_name = "Report_" + datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S') + ".pdf"
    

    return pdf_buffer, file_name

