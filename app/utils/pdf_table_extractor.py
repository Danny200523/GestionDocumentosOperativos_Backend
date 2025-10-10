import pdfplumber
from pdfminer.pdfdocument import PDFPasswordIncorrect

def extract_tables_from_pdf(pdf_file):
    tables_data = []
    try:
        with pdfplumber.open(pdf_file) as pdf:
            for page_number, page in enumerate(pdf.pages, start=1):
                tables = page.extract_tables()
                for table_index, table in enumerate(tables):
                    # Structure table as JSON with position info
                    table_json = {
                        "page": page_number,
                        "table_index": table_index,
                        "data": table  # list of rows, each row is list of cells
                    }
                    tables_data.append(table_json)
    except PDFPasswordIncorrect:
        raise ValueError("El PDF está protegido por contraseña y no se puede procesar.")
    except Exception as e:
        raise ValueError(f"Error al procesar el PDF: {str(e)}")
    return tables_data
