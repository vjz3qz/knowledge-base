from fpdf import FPDF


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
    pdf.output('app/temp/pdfs/report.pdf', 'F')
