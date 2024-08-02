from langchain_community.document_loaders import PyPDFLoader
import pdfplumber

def extract_text_fromaudit(uploaded_file)->str:
    """
    Extract text from uploaded degree audit
    """
    audit_text = []
    # Load PDF
    with pdfplumber.open(uploaded_file) as pdf:
        pages = pdf.pages

        # copy to audit_text
        for page in pages:
            audit_text.append(page.extract_text())


    # remove header from pages 1 to end
    for i in range(1, len(audit_text)):
        start = audit_text[i].find("- In Progress")
        audit_text[i] = audit_text[i][start + 13:]
        # remove last page after Course History
    end = audit_text[-1].find("Course History")
    audit_text[-1] = audit_text[-1][:end]

        # concatenate all pages
    concat_text = ""
    for i in range(len(audit_text)):
        concat_text += audit_text[i]

    return concat_text