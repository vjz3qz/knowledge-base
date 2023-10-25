from fpdf import FPDF
from io import BytesIO

from .document_retriever import upload_to_s3


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
    pdf.output(pdf_buffer, 'F')

    # Reset buffer position to beginning
    pdf_buffer.seek(0)
    
    # Generate a filename (could be based on the content or any other logic you prefer)
    file_name = str(data['Report Type']) + str(data['Employee ID']) + str(data['Date']) + ".pdf"
    
    # TODO GENERATE ID

    # Upload to S3
    unique_id = upload_to_s3(pdf_buffer, file_name=file_name)

    return unique_id

