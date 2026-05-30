

import fitz


def extract_pdf_pages(pdf_path: str):

    doc = fitz.open(pdf_path)

    pages = []

    for page_num, page in enumerate(doc, start=1):

        text = page.get_text()

        pages.append({
            "page": page_num,
            "text": text
        })

    return pages